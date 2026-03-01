
import tkinter
import tkinter.ttk
from uilib.ui.abc import IUI

class UI_Toggle (IUI):

  """トグルボックスを実現する uilib.ui.abc.IUI オブジェクトです。"""

  def __init__ (self, ui:"uilib.ui.abc.IUI"):
    self.ui = ui
    self.int_var = tkinter.IntVar(value=1)
    self.built = None
    self.alt_built = None

  def get_value (self) -> "typing.Any":
    return self.ui.get_value()

  def _rebuild (self):
    if self.int_var.get():
      self.built.grid(column=1, row=0, sticky=tkinter.W)
      self.alt_built.grid_forget()
    else:
      self.built.grid_forget()
      self.alt_built.grid(column=1, row=0, sticky=tkinter.W)

  def _on_change (self):
    self._rebuild()

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":
    base_frame = tkinter.ttk.Frame(master)
    checkbutton = tkinter.ttk.Checkbutton(base_frame, text="", variable=self.int_var, command=self._on_change)
    checkbutton.grid(column=0, row=0, sticky=tkinter.NE)
    built = self.ui.build(base_frame)
    alt_built = tkinter.ttk.Label(base_frame, text="...")
    self.built = built
    self.alt_built = alt_built
    self._rebuild()
    return base_frame

  def load_from_param (self, param:"typing.Any"):
    self.ui.load_from_param(param)

  def save_as_param (self) -> "typing.Any":
    return self.ui.save_as_param()
