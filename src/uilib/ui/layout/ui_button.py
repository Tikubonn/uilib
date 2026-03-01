
import tkinter
import tkinter.ttk
from uilib.ui.abc import IUI

class UI_Button (IUI):

  """任意のボタンを表現する uilib.ui.abc.IUI オブジェクトです。"""

  def __init__ (self, label:str, callback:"typing.Callable[[], None]"):
    self.label = label
    self.callback = callback

  def get_value (self) -> None:
    return None

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":
    base_frame = tkinter.ttk.Frame(master)
    button = tkinter.ttk.Button(base_frame, text=self.label, command=self.callback)
    button.pack(fill=tkinter.X)
    return base_frame

  def load_from_param (self, param:None):
    pass

  def save_as_param (self) -> None:
    return None
