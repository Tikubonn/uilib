
import logging
import tkinter
import tkinter.ttk
import tkinter.filedialog
import operator
import functools 
from enum import Flag
from uilib import const_
from uilib.ui.abc import IUI
from collections import OrderedDict

_LOGGER:logging.Logger = logging.getLogger(__name__)

class UI_Flag (IUI):

  """列挙型(enum.Flag)を表現する UI を提供します。
  """

  def __init__ (
    self, 
    value:"enum.Flag", 
    type_:"typing.Type[enum.Flag]", 
    *,
    calc_key_func:"typing.Callable[[enum.Flag], str]|None"=None,
    readonly:bool=False,
    callback:"typing.Callable[[enum.Flag], None]|None"=None):
    self.type_ = type_
    self.readonly = readonly
    self.callback = callback
    if calc_key_func:
      calc_key_fn = calc_key_func
    else:
      calc_key_fn = lambda flag: flag.name
    label_and_flag = [(calc_key_fn(f), f) for f in type_]
    self.enum_to_label = {f: l for l, f in label_and_flag}
    self.enum_to_var = OrderedDict((f, tkinter.IntVar(value=(f in value))) for _, f in label_and_flag)
    self.label_to_enum = OrderedDict((l, f) for l, f in label_and_flag)

  def get_value (self) -> "enum.Flag":
    enable_flags = (f for f, var in self.enum_to_var.items() if var.get())
    return functools.reduce(operator.or_, enable_flags, self.type_(0))

  def _on_changed (self):
    if self.callback:
      self.callback(self.get_value())

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":
    base_frame = tkinter.ttk.Frame(master, relief=tkinter.GROOVE)
    inner_frame = tkinter.ttk.Frame(base_frame)
    inner_frame.pack(fill=tkinter.X, padx=const_.PADDING_L, pady=const_.PADDING_L)
    for i, (f, var) in enumerate(self.enum_to_var.items()):
      if 0 < i:
        pady = (const_.PADDING, 0)
      else:
        pady = 0
      checkbutton_text = self.enum_to_label[f]
      if self.readonly:
        checkbutton_state = tkinter.DISABLED
      else:
        checkbutton_state = tkinter.NORMAL
      checkbutton = tkinter.ttk.Checkbutton(
        inner_frame, 
        text=checkbutton_text, 
        variable=var,
        command=self._on_changed,
        state=checkbutton_state
      )
      checkbutton.pack(fill=tkinter.X, pady=pady)
    return base_frame

  def load_from_param (self, param:list[str]):
    if isinstance(param, list):
      if not self.readonly:
        for var in self.enum_to_var.values():
          var.set(0)
        for p in param:
          e = self.label_to_enum[p]
          self.enum_to_var[e].set(1)
        self._on_changed()
      else:

        _LOGGER.debug("Ignored loading param because instance is readonly: {!r} <- {!r}".format(self, param)) #log.

    else:
      raise ValueError("Given an invalid param: {!r}".format(param))
  
  def save_as_param (self) -> list[str]:
    return [f.name for f, var in self.enum_to_var.items() if var.get()]
