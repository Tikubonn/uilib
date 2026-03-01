
import tkinter
import tkinter.ttk
from uilib.ui.abc import IUI
from collections import OrderedDict

class UI_Choices (IUI):

  """複数ある候補の中から1つだけを選択する UI を提供します。
  """

  def __init__ (
    self, 
    initial_value:"typing.Any",
    values:"list[typing.Any]",
    calc_key_func:"typing.Callable[[typing.Any], str]"=str,
    callback:"typing.Callable[[typing.Any], None]|None"=None):
    self.callback = callback
    key = calc_key_func(initial_value)
    self.combobox_var = tkinter.StringVar(value=key)
    self.value_table = OrderedDict((
      (calc_key_func(value), value) for value in values
    ))

  def get_value (self) -> "typing.Any":
    key = self.combobox_var.get()
    return self.value_table[key]

  def _on_change (self):
    if self.callback:
      self.callback(self.get_value())

  def _on_combobox_change (self, event:tkinter.Event|None=None):
    self._on_change()

  def build (self, master:tkinter.Widget) -> tkinter.Widget:
    combobox = tkinter.ttk.Combobox(
      textvariable=self.combobox_var,
      values=list(self.value_table.keys()),
      state="readonly"
    )
    combobox.bind("<<ComboboxSelected>>", self._on_combobox_change)
    return combobox

  def load_from_param (self, param:str):
    if isinstance(param, str):
      self.combobox_var.set(param)
      self._on_change()
    else:
      raise ValueError(param)

  def save_as_param (self) -> str:
    return self.combobox_var.get()
