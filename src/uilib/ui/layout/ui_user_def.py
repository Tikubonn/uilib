
from uilib.ui.abc import IUI

class UI_UserDef (IUI):

  """uilib.ui.abc.IUI を継承したクラスを定義することなく UI を作成するためのオブジェクトです。"""

  def __init__ (
    self, 
    *,
    build_func:"typing.Callable[[tkinter.Widget], tkinter.Widget]",
    value_func:"typing.Callable[[], typing.Any]",
    load_func:"typing.Callable[[typing.Any], None]"):
    self.build_func = build_func
    self.value_func = value_func
    self.load_func = load_func

  def get_value (self) -> "typing.Any":
    return self.value_func()

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":
    return self.build_func(master)

  def load_from_param (self, param:"typing.Any"):
    self.load_func(param)
