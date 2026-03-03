
import atexit
import tkinter
import tkinter.messagebox
from enum import Enum, unique, auto
from uilib import global_
from uilib import language
from threading import Thread, RLock
from .dialog import Dialog

@unique
class WorkerStatus (Enum):

  PENDING = auto()
  ABORTED = auto()
  COMPLETED = auto()

class WorkerState:

  """
  """

  def __init__ (self):
    self._progression = 0.0
    self._status = WorkerStatus.PENDING
    self._result = None
    self._lock = RLock()

  @property
  def progression (self) -> float:
    return self._progression

  @property
  def status (self) -> WorkerStatus:
    return self._status

  @property
  def result (self) -> "typing.Any":
    return self._result

  @property
  def lock (self) -> RLock:
    return self._lock

  def set_progression (self, progression:float):

    """
    """

    with self._lock:
      match self._status:
        case WorkerStatus.PENDING:
          if self._progression <= progression:
            self._progression = progression
            if self._progression == 1.0:
              self._status = WorkerStatus.COMPLETED

  def set_result (self, result:"typing.Any"):

    """
    """

    with self._lock:
      match self._status:
        case WorkerStatus.PENDING | WorkerStatus.COMPLETED:
          self._result = result

  def abort (self):

    """
    """

    with self._lock:
      self._status = WorkerStatus.ABORTED

class WorkerDialog (Dialog):

  """
  """

  _REFLESH_RATE:"typing.ClassVar[int]" = 60
  _CLOSE_DELAY_SECONDS:"typing.ClassVar[float]" = 1.0

  def _thread_main (
    self, 
    progression_func:"typing.Callable[[uilib.ui.tkinter_.dialog.worker_dialog.WorkerState], None]", 
    worker_state:WorkerState):
    try:
      progression_func(worker_state)
      worker_state.set_progression(1.0)
    except:
      worker_state.abort()
      raise

  def _after_completed (self):
    self.worker_thread.join()
    self.completion_func(self.worker_state.result)
    self.destroy()

  def _after_loop (self):
    self.update_func(self.worker_state.progression)
    match self.worker_state.status:
      case WorkerStatus.PENDING:
        self.after_id = self.after(1000 // self._REFLESH_RATE, self._after_loop)
      case WorkerStatus.ABORTED:
        pass
      case WorkerStatus.COMPLETED:
        self.after_id = self.after(int(1000 * self._CLOSE_DELAY_SECONDS), self._after_completed)
      case _:
        raise ValueError()

  def _on_destroied (self, event:tkinter.Event):
    if self.after_id:
      self.after_cancel(self.after_id)

  def _on_wm_delete_window (self):
    with self.worker_state.lock:
      self.after_cancel(self.after_id)
      self.after_id = ""
      answer = tkinter.messagebox.askyesno(
        language.translate("DIALOG_WORKER_ABORT_CONFIRMATION_TITLE", self.language),
        language.translate("DIALOG_WORKER_ABORT_CONFIRMATION", self.language)
      )
      if answer:
        self.worker_state.abort()
        self.destroy()
      else:
        self._after_loop()

  def __init__ (
    self, 
    master:tkinter.Widget, 
    setup_func:"typing.Callable[[tkinter.Widget], None]", 
    update_func:"typing.Callable[[float], None]", 
    progression_func:"typing.Callable[[uilib.ui.tkinter_.dialog.worker_dialog.WorkerState], None]", 
    completion_func:"typing.Callable[[typing.Any], None]", 
    *,
    language:dict[str, str]|None=None):

    """
    """

    super().__init__(master, setup_func)
    self.update_func = update_func
    self.completion_func = completion_func
    self.language = language or global_.DEFAULT_LANGUAGE
    self.worker_state = WorkerState()
    self.worker_thread = Thread(target=self._thread_main, args=(progression_func, self.worker_state,))
    self.worker_thread.start()
    atexit.register(self.worker_thread.join)
    self.after_id = ""
    self._after_loop()
    self.bind("<Destroy>", self._on_destroied)
    self.protocol("WM_DELETE_WINDOW", self._on_wm_delete_window)
