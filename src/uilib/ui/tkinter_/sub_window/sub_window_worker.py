
import atexit
import tkinter
import tkinter.messagebox
import traceback
from uilib import global_
from uilib import language
from enum import Enum, auto, unique
from threading import Thread
from .sub_window import SubWindow

@unique
class WorkerStatus (Enum):

  PENDING = auto()
  PAUSED = auto()
  FAILED = auto()
  SUCCEED = auto()

class SubWindow_Worker (SubWindow):

  _REFLESH_RATE:"typing.ClassVar[int]" = 60

  def __after_loop (self):
    match self.__worker_status:
      case WorkerStatus.PENDING:
        self.__widget_update_func()
        self.__after_id = self.after(1000 // self._REFLESH_RATE, self.__after_loop)
      case WorkerStatus.PAUSED:
        self.__after_id = self.after(1000 // self._REFLESH_RATE, self.__after_loop)
      case WorkerStatus.FAILED:
        self.__widget_failed_func()
        self.__thread.join()
        self.destroy()
      case WorkerStatus.SUCCEED:
        self.__widget_succeed_func()
        self.__thread.join()
        self.destroy()
      case _:
        raise ValueError(self.__worker_status) #tmp.

  def __thread_main (self):
    while True:
      match self.__worker_status:
        case WorkerStatus.PENDING:
          try:
            was_satisfied = self.__update_func()
            if was_satisfied:
              match self.__worker_status:
                case WorkerStatus.PENDING | WorkerStatus.PAUSED:
                  self.__worker_status = WorkerStatus.SUCCEED
                case WorkerStatus.FAILED | WorkerStatus.SUCCEED:
                  pass
                case _:
                  raise ValueError(self.__worker_status)
          except:
            self.__worker_status = WorkerStatus.FAILED
            traceback.print_exc() #test.
        case WorkerStatus.PAUSED:
          pass
        case WorkerStatus.FAILED | WorkerStatus.SUCCEED:
          break
        case _:
          raise ValueError(self.__worker_status) #tmp.
    match self.__worker_status:
      case WorkerStatus.FAILED:
        if self.__failed_func:
          self.__failed_func()
      case WorkerStatus.SUCCEED:
        if self.__succeed_func:
          self.__succeed_func()
      case _:
        raise ValueError(self.__worker_status) #tmp.

  def __thread_setup (self):
    self.__thread = Thread(target=self.__thread_main)
    self.__thread.start()
    atexit.register(self.__thread.join)

  def __on_destroy (self, event:"tkinter.Event"):
    match self.__worker_status:
      case WorkerStatus.PENDING | WorkerStatus.PAUSED:
        self.__worker_status = WorkerStatus.FAILED
      case WorkerStatus.FAILED | WorkerStatus.SUCCEED:
        pass
      case _:
        raise ValueError(self.__worker_status)
    if self.__after_id:
      self.after_cancel(self.__after_id)

  def __on_wm_delete_window (self):
    match self.__worker_status:
      case WorkerStatus.PENDING:
        if self.__pause_on_asking:
          self.__worker_status = WorkerStatus.PAUSED
        try:
          answer = tkinter.messagebox.askyesno(
            language.translate("DIALOG_WORKER_ABORT_CONFIRMATION_TITLE", self.__language),
            language.translate("DIALOG_WORKER_ABORT_CONFIRMATION", self.__language)
          )
          if answer:
            self.destroy()
        finally:
          match self.__worker_status:
            case WorkerStatus.PAUSED:
              self.__worker_status = WorkerStatus.PENDING
            case WorkerStatus.PENDING | WorkerStatus.FAILED | WorkerStatus.SUCCEED:
              pass
            case _:
              raise ValueError(self.__worker_status)

  def __init__ (
    self,
    master:"tkinter.Widget",
    setup_func:"typing.Callable[[tkinter.Toplevel], None]",
    *,
    update_func:"typing.Callable[[], bool]",
    failed_func:"typing.Callable[[], None]|None"=None,
    succeed_func:"typing.Callable[[], None]|None"=None,
    widget_update_func:"typing.Callable[[], None]|None"=None,
    widget_failed_func:"typing.Callable[[], None]|None"=None,
    widget_succeed_func:"typing.Callable[[], None]|None"=None,
    language:"dict[str, str]|None"=None,
    is_modal:bool=False,
    pause_on_asking:bool=False):
    super().__init__(master, setup_func, is_modal=is_modal)
    self.__update_func = update_func
    self.__failed_func = failed_func
    self.__succeed_func = succeed_func
    self.__widget_update_func = widget_update_func
    self.__widget_failed_func = widget_failed_func
    self.__widget_succeed_func = widget_succeed_func
    self.__language = language or global_.DEFAULT_LANGUAGE
    self.__pause_on_asking = pause_on_asking
    self.__worker_status = WorkerStatus.PENDING
    self.__after_id = ""
    self.__thread = None
    self.__after_loop()
    self.__thread_setup()
    self.bind("<Destroy>", self.__on_destroy)
    self.protocol("WM_DELETE_WINDOW", self.__on_wm_delete_window)

  @property
  def _worker_status (self) -> WorkerStatus:
    return self.__worker_status

  def join (self):
    self.__thread.join()
