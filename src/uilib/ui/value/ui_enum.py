
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
    calc_key_func:"typing.Callable[[enum.Enum], str]|None"=None,
    readonly:bool=False,
    callback:"typing.Callable[[enum.Enum], None]|None"=None):
    self.type_ = type_
    self.readonly = readonly
    self.callback = callback
    if calc_key_func:
      calc_key_fn = calc_key_func
    else:
      calc_key_fn = lambda enum: enum.name
    label_and_enums = [(calc_key_fn(e), e) for e in type_]
    self.enum_to_label = {e: l for l, e in label_and_enums}
    self.label_to_enum = OrderedDict(((l, e) for l, e in label_and_enums))
    self.var = tkinter.StringVar(value=self.enum_to_label[value])

  def get_value (self) -> "enum.Enum":
    value = self.var.get()
    return self.label_to_enum[value]

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
      values=list(self.label_to_enum.keys()),
      textvariable=self.var,
      state=state,
      width=const_.TEXT_FORM_WIDTH
    )
    combobox.bind("<<ComboboxSelected>>", self._on_combobox_selected)
    return combobox

  def load_from_param (self, param:str):
    if isinstance(param, str):
      if not self.readonly:
        e = self.label_to_enum[param]
        self.var.set(self.enum_to_label[e])
        self._on_changed()
      else:

        _LOGGER.debug("Ignored loading param because instance is readonly: {!r} <- {!r}".format(self, param)) #log.

    else:
      raise ValueError("Given an invalid param: {!r}".format(param))

  def save_as_param (self) -> str:
    return self.var.get()
