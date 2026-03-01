
import tkinter
import tkinter.ttk
import tkinter.filedialog
from uilib import const_
from uilib import image_set
from uilib.ui.abc import IUI

class UI_Path (IUI):

  """ファイルパスを表現する uilib.ui.abc.IUI オブジェクトです。"""

  def __init__ (
    self, 
    value:str, 
    ask_func:"typing.Callable[[], str]"=tkinter.filedialog.askopenfilename,
    callback:"typing.Callable[[str], None]|None"=None):
    self.str_var = tkinter.StringVar(value=value)
    self.ask_func = ask_func
    self.callback = callback
    self.icon_search = None

  def get_value (self) -> str:
    return self.str_var.get()

  def _on_pressed (self):
    path = self.ask_func()
    if path:
      self.str_var.set(path)
      if self.callback:
        self.callback(self.get_value())

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":

    #Load icons.

    self.icon_search = image_set.get_image("icon-search", (12, 12))

    #Main

    base_frame = tkinter.ttk.Frame(master)
    base_frame.columnconfigure(0, weight=1)
    entry = tkinter.ttk.Entry(
      base_frame, 
      textvariable=self.str_var, 
      state=tkinter.DISABLED
    )
    entry.grid(column=0, row=0, sticky=tkinter.EW)
    button = tkinter.ttk.Button(
      base_frame, 
      image=self.icon_search, 
      command=self._on_pressed
    )
    button.grid(column=1, row=0, padx=(const_.PADDING, 0))
    return base_frame

  def load_from_param (self, param:str):
    if isinstance(param, str):
      self.str_var.set(param)
    else:
      raise ValueError(param) #tmp.
  
  def save_as_param (self) -> str:
    return self.str_var.get()
