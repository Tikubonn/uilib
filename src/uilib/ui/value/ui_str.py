
import tkinter
import tkinter.ttk
from uilib import const_
from uilib.ui.abc import IUI

class UI_Str (IUI):

  """任意の文字列を表現する uilib.ui.abc.IUI オブジェクトです。"""

  def __init__ (self, value:str, callback:"typing.Callable[[str], None]|None"=None):
    self.str_var = tkinter.StringVar(value=value)
    self.callback = callback

  def get_value (self) -> str:
    return self.str_var.get()

  def _on_changed (self, event:tkinter.Event|None=None):
    if self.callback:
      self.callback(self.get_value())

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":
    base_frame = tkinter.ttk.Frame(master)
    entry = tkinter.ttk.Entry(
      base_frame, 
      textvariable=self.str_var,
      width=const_.TEXT_FORM_WIDTH
    )
    entry.pack(fill=tkinter.X)
    entry.bind("<FocusOut>", self._on_changed)
    entry.bind("<Return>", self._on_changed)
    return base_frame

  def load_from_param (self, param:str):
    if isinstance(param, str):
      self.str_var.set(param)
      self._on_changed()
    else:
      raise ValueError(param) #tmp.
  
  def save_as_param (self) -> str:
    return self.str_var.get()
