
import tkinter
from uilib import const_
from uilib.ui.abc import IUI

class UI_Button (IUI):

  def __init__ (self, label:str, press_handler:"typing.Callable[[], None]"):
    self.label = label
    self.press_handler = press_handler

  def get_value (self) -> None:
    return None

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":
    base_frame = tkinter.Frame(master)
    button = tkinter.Button(base_frame, text=self.label, command=self.press_handler)
    button.pack(fill=tkinter.X, ipadx=const_.INNER_PADDING)
    return base_frame

  def load_from_param (self, param:"typing.Any"):
    pass
