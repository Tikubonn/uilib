
import tkinter
import tkinter.filedialog
from uilib import const_
from uilib import image_set
from uilib.ui.abc import IUI

class UI_Path (IUI):

  def __init__ (self, value:str, ask_func:"typing.Callable[[], str]"=tkinter.filedialog.askopenfilename):
    self.str_var = tkinter.StringVar(value=value)
    self.ask_func = ask_func

  def get_value (self) -> str:
    return self.str_var.get()

  def _on_pressed (self):
    path = self.ask_func()
    if path:
      self.str_var.set(path)

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":
    base_frame = tkinter.Frame(master)
    base_frame.columnconfigure(0, weight=1)
    entry = tkinter.Entry(base_frame, textvariable=self.str_var, state="readonly", width=const_.TEXT_FORM_WIDTH)
    entry.grid(column=0, row=0, sticky=tkinter.EW, padx=(0, const_.PADDING), ipady=const_.INNER_PADDING)
    button = tkinter.Button(base_frame, image=image_set.get_image("icon-search", (16, 16)), command=self._on_pressed)
    button.grid(column=1, row=0, sticky=tkinter.NS, padx=(const_.PADDING, 0), ipadx=const_.INNER_PADDING)
    return base_frame

  def load_from_param (self, param:str):
    if isinstance(param, str):
      self.str_var.set(param)
    else:
      raise ValueError(param) #tmp.
