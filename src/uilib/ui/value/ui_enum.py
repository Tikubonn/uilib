
import tkinter
import tkinter.filedialog
from enum import Enum
from uilib import const_
from uilib.ui.abc import IUI

class UI_Enum (IUI):

  def __init__ (self, value:"enum.Enum", type_:"typing.Type[enum.Enum]", label_table:"dict[enum.Enum, str]"={}):
    self.type_ = type_
    self.label_table = label_table
    enum_items = tuple(type_)
    self.enum_items = enum_items
    self.int_var = tkinter.IntVar(value=enum_items.index(value))

  def get_value (self) -> "enum.Enum":
    index = self.int_var.get()
    return self.enum_items[index]

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":
    base_frame = tkinter.Frame(master, bd=2, relief=tkinter.GROOVE)
    for i, e in enumerate(self.enum_items):
      radiobutton_text = self.label_table.get(e, e.name)
      radiobutton = tkinter.Radiobutton(base_frame, text=radiobutton_text, variable=self.int_var, value=i)
      radiobutton.grid(column=0, row=i, sticky=tkinter.W, padx=const_.PADDING, pady=const_.PADDING)
    return base_frame

  def load_from_param (self, param:"enum.Enum|int|str"):
    if isinstance(param, Enum):
      index = self.enum_items.index(param)
      self.int_var.set(index)
    elif isinstance(param, int):
      e = self.enum_items[param]
      self.load_from_param(e)
    elif isinstance(param, str):
      e = self.type_(param)
      self.load_from_param(e)
    else:
      raise ValueError(param) #tmp.
