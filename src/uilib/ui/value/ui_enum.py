
import tkinter
import tkinter.ttk
import tkinter.filedialog
from enum import Enum
from uilib import const_
from uilib.ui.abc import IUI
from collections import OrderedDict

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
    enum_table = OrderedDict(((label_table.get(e, e.name), e) for e in type_))
    self.enum_table = enum_table
    self.var = tkinter.StringVar(value=label_table.get(value, value.name))

  def get_value (self) -> "enum.Enum":
    value = self.var.get()
    return self.enum_table[value]

  def _on_changed (self):
    if self.callback:
      self.callback(self.get_value())

  def _on_combobox_selected (self, event:tkinter.Event|None=None):
    self._on_changed()

  def build (self, master:tkinter.Widget) -> tkinter.Widget:
    combobox = tkinter.ttk.Combobox(
      master, 
      values=list(self.enum_table.keys()),
      textvariable=self.var,
      state="readonly",
      width=const_.TEXT_FORM_WIDTH
    )
    combobox.bind("<<ComboboxSelected>>", self._on_combobox_selected)
    return combobox

  def load_from_param (self, param:str):
    if isinstance(param, str):
      e = self.type_[param]
      self.var.set(self.label_table.get(e, e.name))
      self._on_changed()
    else:
      raise ValueError(param) #tmp.

  def save_as_param (self) -> str:
    e = self.get_value()
    return e.name
