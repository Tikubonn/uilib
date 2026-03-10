
import tkinter
import tkinter.ttk
from uilib import const_
from uilib.ui.abc import IUI
from .ui_layout import UI_Layout

class UI_Group (IUI):

  """名前付きグリッドレイアウトを実現します。
  """

  def __init__ (
    self, 
    name:str, 
    uis:list[list[IUI|tuple[IUI, str]|tuple[IUI, str, int]|tuple[IUI, str, int, int]|tuple[IUI, str, int, int, str]|None]], 
    as_single_value:bool=False):

    """インスタンスの初期化を行います。

    Parameters
    ----------
    uis : list[list[IUI|tuple[IUI, str]|tuple[IUI, str, int]|tuple[IUI, str, int, int]|tuple[IUI, str, int, int, str]|None]]
      ウィジットの配置を指示するための2次元配列形式のリストです。
    as_single_value : bool
      本引数が有効ならば get_value メソッドの返り値を辞書ではなく単体の値にします。
      本引数が未指定ならば False が設定されます。
    """

    self.name = name
    self.ui_layout = UI_Layout(uis, as_single_value)

  def get_value (self) -> "dict[str, typing.Any]|typing.Any":
    return self.ui_layout.get_value()

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":
    base_frame = tkinter.ttk.LabelFrame(master, text=self.name)
    built = self.ui_layout.build(base_frame)
    built.pack(fill=tkinter.X, padx=const_.PADDING_L, pady=const_.PADDING_L)
    return base_frame

  def load_from_param (self, param:"list[typing.Any]"):
    self.ui_layout.load_from_param(param)

  def save_as_param (self) -> "list[typing.Any]":
    return self.ui_layout.save_as_param()
