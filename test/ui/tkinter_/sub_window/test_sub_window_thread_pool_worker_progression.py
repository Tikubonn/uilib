
import time
import pytest
import tkinter
import tkinter.ttk
from uilib.ui.tkinter_.sub_window import SubWindow_ThreadPoolWorkerProgression, WorkerStatus, ThreadPoolError
from dataclasses import dataclass

@dataclass(frozen=True)
class Repeat:

  reptition_count:int
  should_raise_error:bool

  def __call__ (self) -> "typing.Generator[float, None, None]":
    if self.should_raise_error:
      raise Exception()
    else:
      for i in range(self.reptition_count):
        yield (i + 1) / self.reptition_count
        time.sleep(1)

@pytest.mark.parametrize(
  [
    "destroy_first",
    "should_raise_error",
    "expect_worker_status",
    "expect_widget_status",
  ],
  [
    pytest.param(
      False,
      False,
      WorkerStatus.SUCCEED,
      WorkerStatus.SUCCEED
    ),
    pytest.param(
      True,
      False,
      WorkerStatus.FAILED,
      WorkerStatus.FAILED
    ),
    pytest.param(
      False,
      True,
      WorkerStatus.FAILED,
      WorkerStatus.FAILED
    )
  ]
)
def test_sub_window_worker_progression (
  test_toplevel:"tkinter.Toplevel",
  destroy_first:bool,
  should_raise_error:bool,
  expect_worker_status:"uilib.ui.tkinter_.sub_window.WorkerStatus",
  expect_widget_status:"uilib.ui.tkinter_.sub_window.WorkerStatus"):
  
  def failed_func (exception:BaseException|None):
    nonlocal worker_status
    nonlocal last_exception
    worker_status = WorkerStatus.FAILED
    last_exception = exception

  def succeed_func ():
    nonlocal worker_status
    worker_status = WorkerStatus.SUCCEED

  def widget_failed_func (exception:BaseException|None):
    nonlocal widget_status
    nonlocal last_exception
    widget_status = WorkerStatus.FAILED
    last_exception = exception

  def widget_succeed_func ():
    nonlocal widget_status
    widget_status = WorkerStatus.SUCCEED

  worker_status = None
  last_exception = None
  widget_status = None
  
  REPEAT_COUNT = 5

  sub_window = SubWindow_ThreadPoolWorkerProgression(
    test_toplevel,
    "Sample title",
    "Sample message",
    update_funcs=[Repeat(i, should_raise_error) for i in range(REPEAT_COUNT)],
    failed_func=failed_func,
    succeed_func=succeed_func,
    widget_failed_func=widget_failed_func,
    widget_succeed_func=widget_succeed_func
  )
  if destroy_first:
    sub_window.destroy()
    sub_window.join()
  else:
    sub_window.join()
    sub_window.destroy()

  assert worker_status is expect_worker_status
  if should_raise_error:
    assert isinstance(last_exception, ThreadPoolError)
    assert len(last_exception.exceptions) == REPEAT_COUNT
  assert widget_status is expect_widget_status
