
import tkinter
import tkinter.filedialog
from enum import Enum
from uilib import const_
from uilib.ui.abc import IUI

class UI_Enum (IUI):

  """列挙型を表現する uilib.ui.abc.IUI オブジェクトです。"""

  def __init__ (
    self, 
    value:"enum.Enum", 
    type_:"typing.Type[enum.Enum]", 
    label_table:"dict[enum.Enum, str]"={},
    callback:"typing.Callable[[enum.Enum], None]|None"=None):
    self.type_ = type_
    self.label_table = label_table
    self.callback = callback
    enum_items = tuple(type_)
    self.enum_items = enum_items
    self.int_var = tkinter.IntVar(value=enum_items.index(value))

  def get_value (self) -> "enum.Enum":
    index = self.int_var.get()
    return self.enum_items[index]

  def _on_change (self):
    if self.callback:
      self.callback(self.get_value())

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":
    base_frame = tkinter.Frame(master, bd=2, relief=tkinter.GROOVE)
    for i, e in enumerate(self.enum_items):
      radiobutton_text = self.label_table.get(e, e.name)
      radiobutton = tkinter.Radiobutton(
        base_frame, 
        text=radiobutton_text, 
        variable=self.int_var, 
        value=i, 
        command=self._on_change
      )
      radiobutton.grid(column=0, row=i, sticky=tkinter.W, padx=const_.PADDING, pady=const_.PADDING)
    return base_frame

  def load_from_param (self, param:str):
    if isinstance(param, str):
      e = self.type_[param]
      index = self.enum_items.index(e)
      self.int_var.set(index)
    else:
      raise ValueError(param) #tmp.

  def save_as_param (self) -> str:
    e = self.get_value()
    return e.name
