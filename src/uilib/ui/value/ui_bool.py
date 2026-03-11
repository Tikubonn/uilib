
import logging
import tkinter
import tkinter.ttk
from uilib.ui.abc import IUI

_LOGGER:logging.Logger = logging.getLogger(__name__)

class UI_Bool (IUI):

  """真偽値を表現する uilib.ui.abc.IUI オブジェクトです。
  """

  def __init__ (
    self, 
    value:bool, 
    readonly:bool=False,
    callback:"typing.Callable[[bool], None]|None"=None):
    self.readonly = readonly
    self.callback = callback
    self.var = tkinter.IntVar(value=value)

  def get_value (self) -> bool:
    return bool(self.var.get())

  def _on_changed (self):
    if self.callback:
      self.callback(self.get_value())

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":
    if self.readonly:
      state = tkinter.DISABLED
    else:
      state = tkinter.NORMAL
    checkbutton = tkinter.ttk.Checkbutton(
      master, 
      variable=self.var, 
      command=self._on_changed,
      state=state
    )
    return checkbutton

  def load_from_param (self, param:bool):
    if isinstance(param, bool):
      if not self.readonly:
        self.var.set(param)
        self._on_changed()
      else:

        _LOGGER.debug("Ignored loading param because instance is readonly: {!r} <- {!r}".format(self, param)) #log.

    else:
      raise ValueError(param) #tmp.
  
  def save_as_param (self) -> bool:
    return bool(self.var.get())
