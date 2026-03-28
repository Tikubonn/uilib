
import tkinter
import tkinter.ttk
from uilib import image_set
from uilib.ui.abc import IUI
from uilib.ui.tkinter_.tooltip import Tooltip

class UI_Hint (IUI):

  def __init__ (self, text:str):
    self.text = text
    self.hint_icon = None

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":

    #load icons.

    self.hint_icon = image_set.get_image("image/icon/hint.png", (16, 16))

    #main

    label = tkinter.ttk.Label(master, image=self.hint_icon)
    Tooltip(label, self.text)
    return label

  def get_value (self) -> None:
    pass

  def load_from_param (self, param:None):
    if param is None:
      pass
    else:
      raise ValueError("Given an invalid param: {!r}".format(param))

  def save_as_param (self) -> None:
    pass
