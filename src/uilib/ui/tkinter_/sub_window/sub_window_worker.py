
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

  """稼働・停止状態のワーカースレッドの動作状態を表現します。

  Attributes
  ----------
  PENDING : Enum
    ワーカースレッドは処理中である。
  PAUSED : Enum
    ワーカースレッドはダイアログによる回答待ち等の理由により一時停止状態である。
  FAILED : Enum
    ワーカースレッドはエラー等の理由により失敗した。
  SUCCEED : Enum
    ワーカースレッドは成功した。
  """

  PENDING = auto()
  PAUSED = auto()
  FAILED = auto()
  SUCCEED = auto()

class SubWindow_Worker (SubWindow):

  """指定された処理に紐づいたサブウィンドウを実現します。

  Attributes
  ----------
  _REFLESH_RATE : typing.ClassVar[int]
    これは秘匿変数です。
    1秒間の間に widget_update_func 関数によりウィジットが更新される回数を表します。
  """

  _REFLESH_RATE:"typing.ClassVar[int]" = 60

  def __after_loop (self):
    match self.__worker_status:
      case WorkerStatus.PENDING:
        if self.__widget_update_func:
          self.__widget_update_func()
        self.__after_id = self.after(1000 // self._REFLESH_RATE, self.__after_loop) #self.after によるループを継続する。
      case WorkerStatus.PAUSED:
        self.__after_id = self.after(1000 // self._REFLESH_RATE, self.__after_loop) #self.after によるループを継続する。
      case WorkerStatus.FAILED:
        if not self.__execed_widget_result_func:
          self.__execed_widget_result_func = True
          # self.__thread.join() #ワーカースレッドに対する待機処理は外部公開している .join メソッドが担当する
          if self.__widget_failed_func:
            self.__widget_failed_func()
          self.destroy()
      case WorkerStatus.SUCCEED:
        if not self.__execed_widget_result_func:
          self.__execed_widget_result_func = True
          # self.__thread.join() #ワーカースレッドに対する待機処理は外部公開している .join メソッドが担当する
          if self.__widget_succeed_func:
            self.__widget_succeed_func()
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
    atexit.register(self.join) #最低でもアプリ終了時に後処理を行わせる

  def __on_destroy (self, event:"tkinter.Event"):
    if self.__after_id:
      self.after_cancel(self.__after_id) #self.after によるループが予約されているならば解除する。
    match self.__worker_status:
      case WorkerStatus.PENDING | WorkerStatus.PAUSED: #途中中断ならば失敗として扱う
        self.__worker_status = WorkerStatus.FAILED
      case WorkerStatus.FAILED | WorkerStatus.SUCCEED: #既に状態が決まっているならば何も行わない
        pass
      case _:
        raise ValueError(self.__worker_status)
    self.__after_loop() #self.__worker_status の値は WorkerStatus.FAILED, WorkerStatus.SUCCEED のいずれかなので1度しか実行されない前提として扱う。

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
              raise ValueError(self.__worker_status) #tmp.

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

    """インスタンスの初期化を行います。

    Parameters
    ----------
    master : tkinter.Widget
      親となるウィジットです。
    setup_func : typing.Callable[[tkinter.Toplevel], None]
      初期化された本インスタンスの画面を作成する関数です。
    update_func : typing.Callable[[], bool]
      ワーカースレッドで繰り返し実行される関数です。
      繰り返し実行を中断し、ワーカー処理を正常終了させるには、本関数の返り値に True を指定します。
    failed_func : typing.Callable[[], None]|None
      ワーカー処理が失敗したと判断された際に実行される関数です。
      本関数はワーカースレッド内で実行されます。
      本引数が未指定の場合 None が設定されます。
    succeed_func : typing.Callable
      ワーカー処理が成功したと判断された際に実行される関数です。
      本関数はワーカースレッド内で実行されます。
      本引数が未指定の場合 None が設定されます。
    widget_update_func : typing.Callable[[], None]|None
      メインスレッドで繰り返し実行される関数です。
      本関数は作成されたサブウィンドウの画面を更新するために利用できます。
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
    self.__execed_widget_result_func = False #widget_failed_func, widget_succeed_func のいずれかが実行されたかを記録する変数
    self.__after_id = ""
    self.__thread = None
    self.__after_loop()
    self.__thread_setup()
    self.bind("<Destroy>", self.__on_destroy)
    self.protocol("WM_DELETE_WINDOW", self.__on_wm_delete_window)

  @property
  def _worker_status (self) -> WorkerStatus:

    """現在のワーカースレッドの状態を取得します。

    Notes
    -----
    本関数・変数は秘匿変数として定義されています。
    そのためサブクラス以外からのアクセスは非推奨です。

    Returns
    -------
    WorkerStatus
      現在のワーカースレッドの状態です。
    """

    return self.__worker_status

  def join (self):

    """本インスタンスのワーカースレッドが終了するまで待機を行います。
    """

    self.__thread.join()
