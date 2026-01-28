
import tkinter
from uilib import const_
from uilib.ui.abc import IUI
from .ui_layout import UI_Layout

class UI_Group (IUI):

  def __init__ (self, name:str, uis:"list[list[uilib.ui.abc.IUI|tuple[uilib.ui.abc.IUI, int]|tuple[uilib.ui.abc.IUI, int, int]|tuple[uilib.ui.abc.IUI, int, int, uilib.enum_.Direction]|None]]", value_uis:"dict[str, uilib.ui.abc.IUI]|uilib.ui.abc.IUI"):
    self.name = name
    self.ui_layout = UI_Layout(uis, value_uis)

  def get_value (self) -> "dict[str, typing.Any]|typing.Any":
    return self.ui_layout.get_value()

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":
    base_frame = tkinter.LabelFrame(master, text=self.name)
    built = self.ui_layout.build(base_frame)
    built.config(bd=0)
    built.pack(fill=tkinter.X, padx=const_.INNER_PADDING, pady=const_.INNER_PADDING)
    return base_frame

  def load_from_param (self, param:"dict[str, typing.Any]|typing.Any"):
    self.ui_layout.load_from_param(param)
