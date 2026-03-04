
import tkinter
import tkinter.messagebox
from uilib import global_
from uilib import language
from threading import Thread
from .sub_window import SubWindow

class SubWindow_Worker (SubWindow):

  """背後で処理を行うサブウィンドウを実現します。
  """

  def _thread_main (self):
    while self.should_continue:
      try:
        self.update_func()
      except:
        traceback.print_exc()
    if self.exit_func:
      self.exit_func()

  def _on_destroied (self, event:"tkinter.Event"):
    self.should_continue = False
    self.thread.join()

  def _on_wm_delete_window (self):
    answer = tkinter.messagebox.askyesno(
      language.translate("DIALOG_WORKER_ABORT_CONFIRMATION_TITLE", self.language),
      language.translate("DIALOG_WORKER_ABORT_CONFIRMATION", self.language)
    )
    if answer:
      self.destroy()

  def __init__ (
    self, 
    master:"tkinter.Widget", 
    setup_func:"typing.Callable[[tkinter.Widget], None]",
    update_func:"typing.Callable[[], None]",
    exit_func:"typing.Callable[[], None]|None"=None,
    *,
    language:"dict[str, str]|None"=None):

    """インスタンスの初期化を行います。

    Parameters
    ----------
    master : tkinter.Widget
      親となる tkinter ウィジットオブジェクトです。
    setup_func : typing.Callable[[tkinter.Widget], None]
      作成される tkinter.Toplevel オブジェクトの初期化を行う関数です。
    update_func : typing.Callable[[], None]
      サブウィンドウの背景で継続して処理される関数です。
    exit_func : typing.Callable[[], None]
      サブウィンドウと update_func が終了する際に呼び出される関数です。
      未指定ならば None が設定されます。
    language : dict[str, str]|None
      幾つかの文章を表示する際に参照される辞書オブジェクトです。
      未指定ならば None が設定されます。
    """

    super().__init__(master, setup_func)
    self.update_func = update_func
    self.exit_func = exit_func
    self.language = language or global_.DEFAULT_LANGUAGE
    self.should_continue = True
    self.thread = Thread(target=self._thread_main)
    self.thread.start()
    self.bind("<Destroy>", self._on_destroied)
    self.protocol("WM_DELETE_WINDOW", self._on_wm_delete_window)
