
import itertools
from typing import Generator
from threading import RLock
from concurrent.futures import ThreadPoolExecutor
from .sub_window_worker import WorkerStatus
from .sub_window_worker_progression import SubWindow_WorkerProgression

class ThreadPoolError (Exception):

  pass

class SubWindow_ThreadPoolWorkerProgression (SubWindow_WorkerProgression):

  def __exec_update_func (self, func:"typing.Callable[[], typing.Generator[float, None, None]]"):
    progressions = func()
    if isinstance(progressions, Generator):
      progressions = itertools.chain(progressions, (1.0,))
      while True:
        match self._worker_status:
          case WorkerStatus.PENDING:
            try:
              progression = next(progressions)
              with self.__lock:
                self.__progression_table[func] = max(self.__progression_table[func], min(1.0, progression))
                self._set_progression(sum(self.__progression_table.values()) / max(1, len(self.__progression_table)))
            except StopIteration:
              break
          case WorkerStatus.PAUSED:
            pass
          case WorkerStatus.FAILED | WorkerStatus.SUCCEED:
            break
          case _:
            raise ValueError(self._worker_status) #tmp.
    else:
      raise ValueError(progressions) #tmp.

  def __update_func (self) -> "typing.Generator[float, None, None]":
    self.__executor = ThreadPoolExecutor()
    features = []
    for func in self.__update_funcs:
      feature = self.__executor.submit(self.__exec_update_func, func)
      features.append(feature)
    while not all((f.done() for f in features)):
      feature_exceptions = {}
      for f in features:
        try:
          exception = f.exception(timeout=0.0)
          if exception:
            feature_exceptions[f] = exception
        except TimeoutError:
          pass
      if feature_exceptions:
        for f in features:
          f.cancel()
        raise ThreadPoolError(feature_exceptions)
    yield 1.0

  def __init__ (
    self,
    master:"tkinter.Widget",
    title:str,
    message:str,
    *,
    update_funcs:"list[typing.Callable[[], typing.Generator[float, None, None]]]",
    failed_func:"typing.Callable[[], None]|None"=None,
    succeed_func:"typing.Callable[[], None]|None"=None,
    widget_failed_func:"typing.Callable[[], None]|None"=None,
    widget_succeed_func:"typing.Callable[[], None]|None"=None,
    language:"dict[str, str]|None"=None,
    is_modal:bool=False,
    pause_on_asking:bool=False):
    self.__update_funcs = update_funcs
    self.__progression_table = {
      func: 0.0 for func in update_funcs
    }
    self.__lock = RLock()
    self.__executor = None
    super().__init__(
      master,
      title,
      message,
      update_func=self.__update_func,
      failed_func=failed_func,
      succeed_func=succeed_func,
      widget_failed_func=widget_failed_func,
      widget_succeed_func=widget_succeed_func,
      language=language,
      is_modal=is_modal,
      pause_on_asking=pause_on_asking
    )

  def join (self):
    if self.__executor:
      self.__executor.shutdown(wait=True)
    super().join()
