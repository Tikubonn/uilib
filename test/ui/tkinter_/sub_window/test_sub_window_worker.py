
import time
import pytest
import tkinter
import tkinter.ttk
from uilib.ui.tkinter_.sub_window import SubWindow_Worker, WorkerStatus

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
def test_sub_window_worker (
  test_toplevel:"tkinter.Toplevel",
  destroy_first:bool,
  should_raise_error:bool,
  expect_worker_status:"uilib.ui.tkinter_.sub_window.WorkerStatus",
  expect_widget_status:"uilib.ui.tkinter_.sub_window.WorkerStatus",
  expect_exception:BaseException|None):
  
  #最低限の動作確認を行います。

  def setup_func (master:"tkinter.Toplevel"):
    label = tkinter.ttk.Label(master, text="Sample label")
    label.pack()

  count_down = 3

  def update_func () -> bool:
    nonlocal count_down
    nonlocal should_raise_error
    if should_raise_error:
      raise expect_exception
    else:
      if 0 < count_down:
        count_down -= 1
        time.sleep(1)
        return False
      else:
        return True

  def failed_func (exception:BaseException|None):
    nonlocal worker_status
    nonlocal last_exception
    worker_status = WorkerStatus.FAILED
    last_exception = exception

  def succeed_func ():
    nonlocal worker_status
    worker_status = WorkerStatus.SUCCEED

  def widget_update_func ():
    pass

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
  
  sub_window = SubWindow_Worker(
    test_toplevel,
    setup_func,
    update_func=update_func,
    failed_func=failed_func,
    succeed_func=succeed_func,
    widget_update_func=widget_update_func,
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
