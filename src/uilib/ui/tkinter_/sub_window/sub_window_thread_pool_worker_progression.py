
import time
import itertools
from typing import Generator
from threading import RLock
from concurrent.futures import ThreadPoolExecutor
from .sub_window_worker import WorkerStatus
from .sub_window_worker_progression import SubWindow_WorkerProgression

class ThreadPoolError (Exception):

  pass

class SubWindow_ThreadPoolWorkerProgression (SubWindow_WorkerProgression):

  """並行処理の進行度を表示するワーカーウィンドウを実現します。
  """

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
    try:
      features = []
      for func in self.__update_funcs:
        feature = self.__executor.submit(self.__exec_update_func, func)
        features.append(feature)
    finally:
      self.__all_submitted = True #この処理が完了するまでの間 .join を実行させてはならない。
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
    pause_on_asking:bool=False,
    ask_on_closing:bool=True):

    """インスタンスの初期化を行います。

    Notes
    -----
    各引数は update_funcs 引数を除いて SubWindow_WorkerProgression と同じです。

    Parameters
    ----------
    master : tkinter.Widget
      親となるウィジットです。
    title : str
      本ウィンドウに表示されるタイトル名です。
    message : str
      本ウィンドウのプログレスバー上部に表示される文章です。
    update_funcs : list[typing.Callable[[], typing.Generator[float, None, None]]]
      ワーカースレッドで1度限り実行される関数の集合です。
      本引数内の関数は concurrent.futures.ThreadPoolExecutor により並行実行されます。
      本クラスは、各関数から返されたジェネレータの各値から、現在の進行度を計算し、画面に表示します。
    failed_func : typing.Callable[[], None]|None
      ワーカー処理が失敗したと判断された際に実行される関数です。
      本関数はワーカースレッド内で実行されます。
      本引数が未指定の場合 None が設定されます。
    succeed_func : typing.Callable
      ワーカー処理が成功したと判断された際に実行される関数です。
      本関数はワーカースレッド内で実行されます。
      本引数が未指定の場合 None が設定されます。
    widget_failed_func : typing.Callable[[], None]|None
      ワーカー処理が失敗した後で実行される関数です。
      本関数はメインスレッド内で実行されます。
      本関数はワーカー処理の実行結果をメッセージボックスで表示するなどの用途に利用することができます。
      本引数が未指定の場合 None が設定されます。
    widget_succeed_func : typing.Callable[[], None]|None
      ワーカー処理が成功した後で実行される関数です。
      本関数はメインスレッド内で実行されます。
      本関数はワーカー処理の実行結果をメッセージボックスで表示するなどの用途に利用することができます。
      本引数が未指定の場合 None が設定されます。
    language : dict[str, str]|None
      本インスタンスが表示するラベルの文章が記録された辞書オブジェクトです。
      本引数が未指定の場合 None が設定されます。
    is_modal : bool
      True が指定されたならば本ウィンドウが閉じられるまで、親ウィンドウへの操作がロックされます。
      本引数が未指定の場合 False が設定されます。
    pause_on_asking : bool
      True が指定されたならば本ウィンドウを閉じるかどうかを確認するダイアログが表示されている間、ワーカー処理を停止します。
      本引数が未指定の場合 False が設定されます。
    """

    self.__update_funcs = update_funcs
    self.__progression_table = {
      func: 0.0 for func in update_funcs
    }
    self.__lock = RLock()
    self.__executor = None
    self.__all_submitted = False
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
      pause_on_asking=pause_on_asking,
      ask_on_closing=ask_on_closing
    )

  def join (self):
    while not self.__all_submitted:
      time.sleep(0) #無意味だったはずだが、スレッドの実行権を別スレッドに委譲するコード。
    if self.__executor:
      self.__executor.shutdown(wait=True)
    super().join() #ThreadPoolExecutor の待機後に親クラスの待機処理に移行します。
