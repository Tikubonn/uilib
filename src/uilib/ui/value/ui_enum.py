
import logging
import tkinter
import tkinter.ttk
import tkinter.filedialog
from enum import Enum
from uilib import const_
from uilib.ui.abc import IUI
from collections import OrderedDict

_LOGGER:logging.Logger = logging.getLogger(__name__)

class UI_Enum (IUI):

  """列挙型を表現する UI を提供します。
  """

  def __init__ (
    self, 
    value:"enum.Enum", 
    type_:"typing.Type[enum.Enum]", 
    *,
    label_table:"dict[enum.Enum, str]"={},
    readonly:bool=False,
    callback:"typing.Callable[[enum.Enum], None]|None"=None):
    self.type_ = type_
    self.label_table = label_table
    self.readonly = readonly
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
    if self.readonly:
      state = tkinter.DISABLED
    else:
      state = "readonly"
    combobox = tkinter.ttk.Combobox(
      master, 
      values=list(self.enum_table.keys()),
      textvariable=self.var,
      state=state,
      width=const_.TEXT_FORM_WIDTH
    )
    combobox.bind("<<ComboboxSelected>>", self._on_combobox_selected)
    return combobox

  def load_from_param (self, param:str):
    if isinstance(param, str):
      if not self.readonly:
        e = self.type_[param]
        self.var.set(self.label_table.get(e, e.name))
        self._on_changed()
      else:

        _LOGGER.debug("Ignored loading param because instance is readonly: {!r} <- {!r}".format(self, param)) #log.

    else:
      raise ValueError(param) #tmp.

  def save_as_param (self) -> str:
    e = self.get_value()
    return e.name
