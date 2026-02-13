
import tkinter
import tkinter.filedialog
import operator
import functools 
from enum import Flag
from uilib import const_
from uilib.ui.abc import IUI
from collections import OrderedDict

class UI_Flag (IUI):

  """列挙型(enum.Flag)を表現する uilib.ui.abc.IUI オブジェクトです。"""

  def __init__ (
    self, 
    value:"enum.Flag", 
    type_:"typing.Type[enum.Flag]", 
    label_table:"dict[enum.Flag, str]"={},
    callback:"typing.Callable[[enum.Flag], None]|None"=None):
    self.type_ = type_
    self.label_table = label_table
    self.callback = callback
    self.int_var_table = OrderedDict(((f, tkinter.IntVar(value=(f in value))) for f in type_))

  def get_value (self) -> "enum.Flag":
    enable_flags = (f for f, var in self.int_var_table.items() if var.get())
    return functools.reduce(operator.or_, enable_flags, self.type_(0))

  def _on_change (self):
    if self.callback:
      self.callback(self.get_value())

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":
    base_frame = tkinter.Frame(master, bd=2, relief=tkinter.GROOVE)
    for f, var in self.int_var_table.items():
      checkbutton_text = self.label_table.get(f, f.name)
      checkbutton = tkinter.Checkbutton(
        base_frame, 
        text=checkbutton_text, 
        variable=var,
        command=self._on_change
      )
      checkbutton.pack(fill=tkinter.X, padx=const_.PADDING, pady=const_.PADDING)
    return base_frame

  def load_from_param (self, param:list[str]):
    if isinstance(param, list):
      for var in self.int_var_table.values():
        var.set(0)
      for p in param:
        e = self.type_[p]
        self.int_var_table[e].set(1)
    else:
      raise ValueError(param) #tmp.
  
  def save_as_param (self) -> list[str]:
    return [f.name for f, var in self.int_var_table.items() if var.get()]
