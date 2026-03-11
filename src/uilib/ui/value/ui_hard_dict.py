
import tkinter
import tkinter.ttk
from uilib import const_
from uilib.ui.abc import IUI
from collections import OrderedDict

class UI_HardDict (IUI):

  """固定された要素をもつ辞書を表現する UI を提供します。
  """

  def __init__ (
    self, 
    uis:dict[str, IUI]|list[tuple[str, IUI]], 
    *,
    label_table:dict[str, str]={}):
    self.uis = OrderedDict(uis)
    self.label_table = label_table

  def get_value (self) -> "dict[str, typing.Any]":
    return {
      key: ui.get_value() for key, ui in self.uis.items()
    }

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":
    base_frame = tkinter.ttk.Frame(master)
    for i, (key, ui) in enumerate(self.uis.items()):
      if 0 < i:
        pady = (const_.PADDING, 0)
      else:
        pady = 0
      label_text = self.label_table.get(key, key)
      label = tkinter.ttk.Label(base_frame, text=label_text)
      label.grid(column=0, row=i, sticky=tkinter.NE, pady=pady)
      built = ui.build(base_frame)
      built.grid(column=1, row=i, sticky=tkinter.W, padx=(const_.PADDING, 0), pady=pady)
    return base_frame

  def load_from_param (self, param:"dict[str, typing.Any]"):
    if isinstance(param, dict):
      for key, inner_param in param.items():
        self.uis[key].load_from_param(inner_param)
    else:
      raise ValueError(param) #tmp.

  def save_as_param (self) -> "dict[str, typing.Any]":
    return {
      key: ui.save_as_param() for key, ui in self.uis.items()
    }
