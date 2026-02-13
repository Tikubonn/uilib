
import tkinter
from uilib import enum_
from uilib import const_
from uilib.ui.abc import IUI
from typing import NamedTuple

class _CellInfo (NamedTuple):

  ui:"uilib.ui.abc.IUI|None"
  column_span:int = 1
  row_span:int = 1
  align:"uilib.enum_.Direction" = enum_.Direction.W

  @classmethod
  def from_param (cls, param:"uilib.ui.abc.IUI|tuple[uilib.abc.IUI, int]|tuple[uilib.abc.IUI, int, int]|tuple[uilib.ui.abc.IUI, int, int, uilib.enum_.Direction]|None") -> "typing.Self":
    if isinstance(param, IUI):
      return cls(param)
    elif isinstance(param, tuple):
      match len(param):
        case 2:
          ui, column_span = param
          return cls(ui, column_span)
        case 3:
          ui, column_span, row_span = param
          return cls(ui, column_span, row_span)
        case 4:
          ui, column_span, row_span, align = param
          return cls(ui, column_span, row_span, align)
        case _:
          raise ValueError(param) #tmp.
    elif param is None:
      return cls(None)
    else:
      raise ValueError(param) #tmp.

class UI_Layout (IUI):

  """レイアウトを実現する uilib.ui.abc.IUI オブジェクトです。"""

  def __init__ (self, uis:"list[list[uilib.ui.abc.IUI|tuple[uilib.ui.abc.IUI, int]|tuple[uilib.ui.abc.IUI, int, int]|tuple[uilib.ui.abc.IUI, int, int, uilib.enum_.Direction]|None]]", value_uis:"dict[str, uilib.ui.abc.IUI]|uilib.ui.abc.IUI"):
    self.uis = uis
    self.value_uis = value_uis

  def get_value (self) -> "list[typing.Any]":
    if isinstance(self.value_uis, dict):
      return {key: ui.get_value() for key, ui in self.value_uis.items()}
    elif isinstance(self.value_uis, IUI):
      return self.value_uis.get_value()
    else:
      raise ValueError(self.value_uis) #tmp.

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":
    cell_infos = [
      [
        _CellInfo.from_param(ui) for ui in inner_uis
      ] for inner_uis in self.uis
    ]
    base_frame = tkinter.Frame(master, bd=2, relief=tkinter.GROOVE)
    row = 0
    for inner_cell_infos in cell_infos:
      if row == 0:
        pady = (0, const_.PADDING)
      elif row +1 < len(cell_infos):
        pady = (const_.PADDING, 0)
      else:
        pady = const_.PADDING
      column = 0
      for cell_info in inner_cell_infos:
        if column == 0:
          padx = (0, const_.PADDING)
        elif column +1 < len(inner_cell_infos):
          padx = (const_.PADDING, 0)
        else:
          padx = const_.PADDING
        if cell_info.ui:
          match cell_info.align:
            case enum_.Direction.E:
              sticky = tkinter.E
            case enum_.Direction.W:
              sticky = tkinter.W
            case enum_.Direction.E | enum_.W:
              sticky = tkinter.EW
            case _:
              sticky = tkinter.W
          built = cell_info.ui.build(base_frame)
          built.grid(
            column=column, 
            columnspan=cell_info.column_span, 
            row=row, 
            rowspan=cell_info.row_span, 
            sticky=sticky,
            padx=padx, 
            pady=pady
          )
        column += cell_info.column_span
      row += min((cell_info.row_span for cell_info in inner_cell_infos), default=0)
    return base_frame

  def load_from_param (self, param:"dict[str, typing.Any]|typing.Any"):
    if isinstance(self.value_uis, dict):
      if isinstance(param, dict):
        for key, inner_param in param.items():
          if key in self.value_uis:
            self.value_uis[key].load_from_param(inner_param)
          else:
            raise KeyError(param) #tmp.
      else:
        raise ValueError(param) #tmp.
    elif isinstance(self.value_uis, IUI):
      self.value_uis.load_from_param(param)
    else:
      raise ValueError(param) #tmp.
