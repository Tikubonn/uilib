
import tkinter
from uilib import const_
from uilib.ui.abc import IUI

class UI_Text (IUI):

  def __init__ (self, text:str):
    self.text = text
    self.base_frame = None
    self.message = None

  def get_value (self) -> None:
    return None

  def _on_resize (self, event:"tkinter.Event|None"=None):
    self.message.config(width=self.base_frame.winfo_width())

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":
    base_frame = tkinter.Frame(master)
    base_frame.bind("<Configure>", self._on_resize)
    message = tkinter.Message(base_frame, text=self.text)
    message.pack(anchor=tkinter.W)
    self.base_frame = base_frame
    self.message = message
    self._on_resize()
    return base_frame

  def load_from_param (self, params:None):
    pass
