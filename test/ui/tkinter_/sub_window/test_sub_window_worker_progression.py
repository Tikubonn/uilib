
import time
import pytest
import tkinter
import tkinter.ttk
from uilib.ui.tkinter_.sub_window import SubWindow_WorkerProgression, WorkerStatus

@pytest.mark.parametrize(
  [
    "destroy_first",
    "should_raise_error",
    "expect_worker_status",
    "expect_widget_status",
    "expect_exception",
  ],
  [
    pytest.param(
      False,
      False,
      WorkerStatus.SUCCEED,
      WorkerStatus.SUCCEED,
      None
    ),
    pytest.param(
      True,
      False,
      WorkerStatus.FAILED,
      WorkerStatus.FAILED,
      None
    ),
    pytest.param(
      False,
      True,
      WorkerStatus.FAILED,
      WorkerStatus.FAILED,
      Exception()
    )
  ]
)
def test_sub_window_worker_progression (
  test_toplevel:"tkinter.Toplevel",
  destroy_first:bool,
  should_raise_error:bool,
  expect_worker_status:"uilib.ui.tkinter_.sub_window.WorkerStatus",
  expect_widget_status:"uilib.ui.tkinter_.sub_window.WorkerStatus",
  expect_exception:BaseException|None):
  
  def update_func () -> "typing.Generator[float, None, None]":
    nonlocal should_raise_error
    if should_raise_error:
      raise expect_exception
    else:

      TOTAL_COUNT = 3

      for i in range(TOTAL_COUNT):
        yield (i + 1) / TOTAL_COUNT
        time.sleep(1)

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

  sub_window = SubWindow_WorkerProgression(
    test_toplevel,
    "Sample title",
    "Sample message",
    update_func=update_func,
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
  assert last_exception is expect_exception
  assert widget_status is expect_widget_status
