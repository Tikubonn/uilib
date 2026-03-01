
import tkinter
import tkinter.ttk
from uilib import const_
from uilib.ui.abc import IUI
from collections import OrderedDict

class UI_Tab (IUI):

  def __init__ (self, uis:"dict[str, uilib.ui.abc.IUI]"):
    self.uis = OrderedDict(uis)

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
      notebook.add(content_frame, text=key)
    return notebook

  def load_from_param (self, param:"dict[str, typing.Any]"):
    if isinstance(param, dict):
      for key, inner_param in self.uis.items():
        ui = self.uis[key]
        ui.load_from_param(inner_param)
    else:
      raise ValueError(param) #tmp.

  def save_as_param (self) -> "dict[str, typing.Any]":
    return {
      key: ui.save_as_param() for key, ui in self.uis.items()
    }
