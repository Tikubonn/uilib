
import tkinter
import tkinter.ttk
from uilib import const_
from uilib.ui.abc import IUI
from collections import OrderedDict

class UI_Tab (IUI):

  def __init__ (
    self, 
    uis:"dict[str, uilib.ui.abc.IUI]",
    label_table:dict[str, str]={}):
    self.uis = OrderedDict(uis)
    self.label_table = label_table

  def get_value (self) -> "dict[str, typing.Any]":
    return {
      key: ui.get_value() for key, ui in self.uis.items()
    }

  def build (self, master:tkinter.Widget) -> tkinter.Widget:
    notebook = tkinter.ttk.Notebook(master)
    for key, ui in self.uis.items():
      content_frame = tkinter.ttk.Frame(notebook)
      content_frame.pack(fill=tkinter.X)
      built = ui.build(content_frame)
      built.pack(anchor=tkinter.W, padx=const_.PADDING_L, pady=const_.PADDING_L)
      tab_text = self.label_table.get(key, key)
      notebook.add(content_frame, text=tab_text)
    return notebook

  def load_from_param (self, param:"dict[str, typing.Any]"):
    if isinstance(param, dict):
      for key, inner_param in param.items():
        ui = self.uis[key]
        ui.load_from_param(inner_param)
    else:
      raise ValueError(param) #tmp.

  def save_as_param (self) -> "dict[str, typing.Any]":
    return {
      key: ui.save_as_param() for key, ui in self.uis.items()
    }
