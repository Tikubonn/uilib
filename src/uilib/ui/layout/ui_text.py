
import tkinter
import tkinter.ttk
from uilib import const_
from uilib.ui.abc import IUI

class UI_Text (IUI):

  """複数行にわたるテキストラベルを実現する uilib.ui.abc.IUI オブジェクトです。"""

  def __init__ (self, text:str):
    self.text = text
    self.base_frame = None
    self.message = None

  def get_value (self) -> None:
    return None

  def _on_resize (self, event:"tkinter.Event|None"=None):
    self.message.config(width=self.base_frame.winfo_width())

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":
    base_frame = tkinter.ttk.Frame(master)
    base_frame.bind("<Configure>", self._on_resize)
    message = tkinter.Message(
      base_frame, 
      text=self.text, 
      bd=0, #広範囲の余白を削除する
      pady=0, #縦方向の小範囲の余白を削除する
    )
    message.pack(anchor=tkinter.W)
    self.base_frame = base_frame
    self.message = message
    self._on_resize()
    return base_frame

  def load_from_param (self, params:None):
    if param is None:
      pass
    else:
      raise ValueError("Given an invalid param: {!r}".format(param))

  def save_as_param (self) -> None:
    return None
