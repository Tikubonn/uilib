
import tkinter
import tkinter.ttk
from uilib.ui.abc import IUI

class _UI_Number (IUI):

  def __init__ (
    self, 
    var:"tkinter.Variable", 
    value_range_step:"tuple[typing.Any, typing.Any, typing.Any]|None"=None,
    callback:"typing.Callable[[typing.Any], None]|None"=None):
    self.var = var
    self.value_range_step = value_range_step
    self.callback = callback

  def get_value (self) -> "typing.Any":
    return self.var.get()

  def _on_change (self, event:tkinter.Event|None=None):
    if self.callback:
      self.callback(self.get_value())

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":
    base_frame = tkinter.ttk.Frame(master)
    if self.value_range_step:
      min_, max_, step = self.value_range_step
      spinbox = tkinter.ttk.Spinbox(
        base_frame, 
        from_=min_, 
        to=max_, 
        increment=step, 
        textvariable=self.var,
        command=self._on_change
      )
      spinbox.pack(fill=tkinter.X)
      spinbox.bind("<FocusOut>", self._on_change)
      spinbox.bind("<Return>", self._on_change)
    else:
      entry = tkinter.ttk.Entry(
        base_frame, 
        textvariable=self.var
      )
      entry.pack(fill=tkinter.X)
      entry.bind("<FocusOut>", self._on_change)
      entry.bind("<Return>", self._on_change)
    return base_frame

  def load_from_param (self, param:"typing.Any"):
    self.var.set(param)

  def save_as_param (self) -> "typing.Any":
    return self.var.get()

class UI_Int (IUI):

  """整数を表現する uilib.ui.abc.IUI オブジェクトです。"""

  def __init__ (
    self, 
    value:int, 
    value_range_step:tuple[int, int, int]|None=None,
    callback:"typing.Callable[[int], None]|None"=None):
    var = tkinter.IntVar(value=value)
    self.ui_number = _UI_Number(var, value_range_step, callback)

  def get_value (self) -> int:
    return self.ui_number.get_value()

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":
    return self.ui_number.build(master)

  def load_from_param (self, param:int):
    if isinstance(param, int):
      self.ui_number.load_from_param(param)
    else:
      raise ValueError(param) #tmp.

  def save_as_param (self) -> int:
    return self.ui_number.save_as_param()

class UI_Float (IUI):

  """浮動小数点数を表現する uilib.ui.abc.IUI オブジェクトです。"""

  def __init__ (
    self, 
    value:float, 
    value_range_step:tuple[float, float, float]|None=None,
    callback:"typing.Callable[[float], None]|None"=None):
    var = tkinter.DoubleVar(value=value)
    self.ui_number = _UI_Number(var, value_range_step, callback)

  def get_value (self) -> float:
    return self.ui_number.get_value()

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":
    return self.ui_number.build(master)

  def load_from_param (self, param:float):
    if isinstance(param, float):
      self.ui_number.load_from_param(param)
    else:
      raise ValueError(param) #tmp.

  def save_as_param (self) -> float:
    return self.ui_number.save_as_param()
