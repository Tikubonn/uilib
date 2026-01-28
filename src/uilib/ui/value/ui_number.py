
import tkinter
from uilib import const_
from uilib.ui.abc import IUI

class _UI_Number (IUI):

  def __init__ (self, var:"tkinter.Variable", value_range_step:"tuple[typing.Any, typing.Any, typing.Any]|None"=None):
    self.var = var
    self.value_range_step = value_range_step

  def get_value (self) -> "typing.Any":
    return self.var.get()

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":
    base_frame = tkinter.Frame(master)
    if self.value_range_step:
      min_, max_, step = self.value_range_step
      spinbox = tkinter.Spinbox(base_frame, from_=min_, to=max_, increment=step, textvariable=self.var, width=const_.NUMERIC_FORM_WIDTH)
      spinbox.pack(fill=tkinter.X, ipady=const_.INNER_PADDING)
    else:
      entry = tkinter.Entry(base_frame, textvariable=self.var, width=const_.NUMERIC_FORM_WIDTH)
      entry.pack(fill=tkinter.X, ipady=const_.INNER_PADDING)
    return base_frame

  def load_from_param (self, param:"typing.Any"):
    self.var.set(param)

class UI_Int (IUI):

  def __init__ (self, value:int, value_range_step:tuple[int, int, int]|None=None):
    var = tkinter.IntVar(value=value)
    self.ui_number = _UI_Number(var, value_range_step)

  def get_value (self) -> int:
    return self.ui_number.get_value()

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":
    return self.ui_number.build(master)

  def load_from_param (self, param:int):
    if isinstance(param, int):
      self.ui_number.load_from_param(param)
    else:
      raise ValueError(param) #tmp.

class UI_Float (IUI):

  def __init__ (self, value:float, value_range_step:tuple[float, float, float]|None=None):
    var = tkinter.DoubleVar(value=value)
    self.ui_number = _UI_Number(var, value_range_step)

  def get_value (self) -> float:
    return self.ui_number.get_value()

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":
    return self.ui_number.build(master)

  def load_from_param (self, param:float):
    if isinstance(param, float):
      self.ui_number.load_from_param(param)
    else:
      raise ValueError(param) #tmp.
