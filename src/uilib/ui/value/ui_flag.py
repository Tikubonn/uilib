
import tkinter
import tkinter.filedialog
import operator
import functools 
from enum import Flag
from uilib import const_
from uilib.ui.abc import IUI
from collections import OrderedDict

class UI_Flag (IUI):

  def __init__ (self, value:"enum.Flag", type_:"typing.Type[enum.Flag]", label_table:"dict[enum.Flag, str]"={}):
    self.type_ = type_
    self.label_table = label_table
    self.int_var_table = OrderedDict(((f, tkinter.IntVar(value=(f in value))) for f in type_))

  def get_value (self) -> "enum.Flag":
    enable_flags = (f for f, var in self.int_var_table.items() if var.get())
    return functools.reduce(operator.or_, enable_flags, self.type_(0))

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":
    base_frame = tkinter.Frame(master, bd=2, relief=tkinter.GROOVE)
    for f, var in self.int_var_table.items():
      checkbutton_text = self.label_table.get(f, f.name)
      checkbutton = tkinter.Checkbutton(base_frame, text=checkbutton_text, variable=var)
      checkbutton.pack(fill=tkinter.X, padx=const_.PADDING, pady=const_.PADDING)
    return base_frame

  def load_from_param (self, param:"enum.Flag|int|str"):
    if isinstance(param, Flag):
      for f, var in self.int_var_table.items():
        var.set((f in param))
    elif isinstance(param, int):
      f = self.type_(param)
      self.load_from_param(f)
    elif isinstance(param, str):
      f = self.type_[param]
      self.load_from_param(f)
    else:
      raise ValueError(param) #tmp.
