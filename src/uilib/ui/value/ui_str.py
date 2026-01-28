
import tkinter
from uilib import const_
from uilib.ui.abc import IUI

class UI_Str (IUI):

  def __init__ (self, value:str):
    self.str_var = tkinter.StringVar(value=value)

  def get_value (self) -> str:
    return self.str_var.get()

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":
    base_frame = tkinter.Frame(master)
    entry = tkinter.Entry(base_frame, textvariable=self.str_var, width=const_.TEXT_FORM_WIDTH)
    entry.pack(fill=tkinter.X, expand=True, ipadx=const_.INNER_PADDING, ipady=const_.INNER_PADDING)
    return base_frame

  def load_from_param (self, param:str):
    if isinstance(param, str):
      self.str_var.set(param)
    else:
      raise ValueError(param) #tmp.
