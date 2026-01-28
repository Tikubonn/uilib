
import tkinter
from uilib.ui.abc import IUI

class UI_Bool (IUI):

  def __init__ (self, value:bool):
    self.int_var = tkinter.IntVar(value=value)

  def get_value (self) -> bool:
    return bool(self.int_var.get())

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":
    checkbutton = tkinter.Checkbutton(master, variable=self.int_var)
    return checkbutton

  def load_from_param (self, param:bool):
    if isinstance(param, bool):
      self.int_var.set(param)
    else:
      raise ValueError(param) #tmp.
