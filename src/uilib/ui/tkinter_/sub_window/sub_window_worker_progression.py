
import tkinter
import tkinter.ttk
import logging
import itertools
from uilib import const_
from typing import Generator
from .sub_window_worker import SubWindow_Worker, WorkerStatus

_LOGGER:"logging.Logger" = logging.getLogger(__name__)

class SubWindow_WorkerProgression (SubWindow_Worker):

  """プログレスバーによる進行度の表示を行うワーカーウィンドウを実現します。

  Notes
  -----
  本クラスはファイルのダウンロードなど1度限り実行される処理を視覚化するために実装されました。
  そのため、サーバ等の継続的な処理を必要とするものに関しては SubWindow_Worker の利用を検討してください。

  Attributes
  ----------
  _MAX_PROGRESSION_VALUE : typing.ClassVar[int]
    これは秘匿変数です。
    tkinter.ttk.Progressbar インスタンスの最大値となる整数です。
  """

  _MAX_PROGRESSION_VALUE:"typing.ClassVar[int]" = 1000

  def __update_progression_text (self):
    progression_int = self.__progression_var.get()
    self.__progression_label_var.set("{:>5.1f}%".format(progression_int / self._MAX_PROGRESSION_VALUE * 100.0))

  def __setup_func (self, master:"tkinter.Toplevel"):
    master.title(self.__title)
    base_frame = tkinter.ttk.Frame(master)
    base_frame.pack(padx=const_.PADDING_L, pady=const_.PADDING_L)
    message_label = tkinter.ttk.Label(base_frame, text=self.__message)
    message_label.grid(column=0, columnspan=2, row=0, sticky=tkinter.EW)
    progression_label = tkinter.ttk.Label(base_frame, textvariable=self.__progression_label_var)
    progression_label.grid(column=0, row=1, sticky=tkinter.E, pady=(const_.PADDING_L, 0))
    progression_bar = tkinter.ttk.Progressbar(base_frame, orient=tkinter.HORIZONTAL, variable=self.__progression_var, maximum=self._MAX_PROGRESSION_VALUE)
    progression_bar.grid(column=1, row=1, sticky=tkinter.EW, pady=(const_.PADDING_L, 0), padx=(const_.PADDING, 0))
    self.__update_progression_text()

  def _set_progression (self, progression:float):

    """本インスタンスの現在の進行度を設定します。

    Notes
    -----
    progression の値が現在進行度よりも小さいもしくは 1.0 よりも大きい場合、
    その値は 0.0 ~ 1.0 までの範囲に収められます。

    メソッドは秘匿関数として定義されています。
    そのためサブクラス以外からのアクセスは非推奨です。

    Parameters
    ----------
    progression : float
      新しい進行度を表す 0.0 ~ 1.0 までの範囲の浮動小数点数です。
    """

    self.__cur_progression = max(self.__cur_progression, min(1.0, progression))

    _LOGGER.debug("Set progression: {:1.3f}".format(self.__cur_progression)) #log.

  def __wrapped_update_func (self):
    progressions = self.__update_func()
    if isinstance(progressions, Generator):
      progressions = itertools.chain(progressions, (1.0,))
      while True:
        match self._worker_status:
          case WorkerStatus.PENDING:
            try:
              progression = next(progressions)
              self._set_progression(progression)
            except StopIteration:
              break
          case WorkerStatus.PAUSED:
            pass
          case WorkerStatus.FAILED | WorkerStatus.SUCCEED:
            break
          case _:
            raise ValueError(self._worker_status)
      return True #Don't repeat again.
    else:
      raise ValueError(progressions) #tmp.

  def __widget_update_func (self):
    progression_int = round(self.__cur_progression * self._MAX_PROGRESSION_VALUE)
    self.__progression_var.set(progression_int)
    self.__update_progression_text()

  def __init__ (
    self,
    master:"tkinter.Widget",
    title:str,
    message:str,
    *,
    update_func:"typing.Callable[[], typing.Generator[float, None, None]]|None",
    failed_func:"typing.Callable[[], None]|None"=None,
    succeed_func:"typing.Callable[[], None]|None"=None,
    widget_failed_func:"typing.Callable[[], None]|None"=None,
    widget_succeed_func:"typing.Callable[[], None]|None"=None,
    language:"dict[str, str]|None"=None,
    is_modal:bool=False,
    pause_on_asking:bool=False,
    ask_on_closing:bool=True):

    """インスタンスの初期化を行います。

    Parameters
    ----------
    master : tkinter.Widget
      親となるウィジットです。
    title : str
      本ウィンドウに表示されるタイトル名です。
    message : str
      本ウィンドウのプログレスバー上部に表示される文章です。
    update_func : typing.Callable[[], typing.Generator[float, None, None]]
      ワーカースレッドで1度限り実行される関数です。
      本クラスは、本関数から返されたジェネレータの各値を、現在の進行度として画面に表示します。
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

    self.__title = title
    self.__message = message
    self.__update_func = update_func
    self.__progression_var = tkinter.IntVar(value=0)
    self.__progression_label_var = tkinter.StringVar(value="")
    self.__cur_progression = 0.0
    super().__init__(
      master,
      self.__setup_func,
      update_func=self.__wrapped_update_func,
      failed_func=failed_func,
      succeed_func=succeed_func,
      widget_update_func=self.__widget_update_func,
      widget_failed_func=widget_failed_func,
      widget_succeed_func=widget_succeed_func,
      language=language,
      is_modal=is_modal,
      pause_on_asking=pause_on_asking,
      ask_on_closing=ask_on_closing
    )
