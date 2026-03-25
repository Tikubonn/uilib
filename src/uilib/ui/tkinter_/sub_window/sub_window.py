
import tkinter

class SubWindow (tkinter.Toplevel):

  """tkinter によるサブウィンドウを実現します。
  """

  def __init__ (
    self,
    master:"tkinter.Widget",
    setup_func:"typing.Callable[[tkinter.Toplevel], None]",
    *,
    is_modal:bool=False):

    """インスタンスの初期化を行います。

    Parameters
    ----------
    master : tkinter.Widget
      親となるウィジットです。
    setup_func : typing.Callable[[tkinter.Toplevel], None]
      初期化された本インスタンスの画面を作成する関数です。
    is_modal : bool
      True が指定されたならば本ウィンドウが閉じられるまで、親ウィンドウへの操作がロックされます。
    """

    super().__init__(master)
    setup_func(self)
    if is_modal:
      self.transient(master) #tkinter.Toplevel.wm_attributes("-topmost", 1)
      self.grab_set()
