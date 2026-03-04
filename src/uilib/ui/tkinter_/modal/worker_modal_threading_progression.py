
import traceback
from threading import RLock
from concurrent.futures import ThreadPoolExecutor
from .worker_modal_progression import WorkerModal_Progression

class WorkerModal_ThreadingProgression (WorkerModal_Progression):

  def _exec_progression_func (
    self, 
    func:"typing.Callable[[...], None]", 
    worker_state:"uilib.ui.tkinter_.modal.worker_modal.WorkerState") -> "typing.Any":
    try:
      result = func(*self.args, **self.kwargs)
      with self.lock:
        self.completion_count += 1
        worker_state.set_progression(self.completion_count / len(self.progression_funcs))
      return result
    except:
      traceback.print_exc()
      worker_state.abort()

  def _progression_func (
    self, 
    worker_state:"uilib.ui.tkinter_.modal.worker_modal.WorkerState"):
    with ThreadPoolExecutor() as executor:
      futures = []
      for func in self.progression_funcs:
        future = executor.submit(self._exec_progression_func, func, worker_state)
        futures.append(future)
      results = [f.result() for f in futures]
      worker_state.set_result(results)

  def __init__ (
    self, 
    master:"tkinter.Widget", 
    title:str, 
    message:str, 
    progression_funcs:"typing.Callable[[...], None]", 
    completed_func:"typing.Callable[[Any], None]", 
    *, 
    args:"tuple[typing.Any]"=(), 
    kwargs:"dict[str, typing.Any]"={}, 
    language:"dict[str, str]|None"=None):
    self.progression_funcs = progression_funcs
    self.args = args
    self.kwargs = kwargs
    self.lock = RLock()
    self.completion_count = 0
    super().__init__(
      master,
      title,
      message,
      self._progression_func,
      completed_func,
      language=language
    )
