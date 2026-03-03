
import tkinter
import tkinter.ttk
from uilib.ui.abc import IUI

class UI_Bool (IUI):

  """真偽値を表現する uilib.ui.abc.IUI オブジェクトです。
  """

  def __init__ (self, value:bool, callback:"typing.Callable[[bool], None]|None"=None):
    self.var = tkinter.IntVar(value=value)
    self.callback = callback

  def get_value (self) -> bool:
    return bool(self.var.get())

  def _on_changed (self):
    if self.callback:
      self.callback(self.get_value())

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":
    checkbutton = tkinter.ttk.Checkbutton(master, variable=self.var, command=self._on_changed)
    return checkbutton

  def load_from_param (self, param:bool):
    if isinstance(param, bool):
      self.var.set(param)
      self._on_changed()
    else:
      raise ValueError(param) #tmp.
  
  def save_as_param (self) -> bool:
    return bool(self.var.get())
