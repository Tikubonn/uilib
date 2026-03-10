
import tkinter
import tkinter.ttk
import itertools
from uilib import const_
from uilib.ui.abc import IUI
from typing import NamedTuple

class _CellInfo (NamedTuple):

  ui:"uilib.ui.abc.IUI|None"
  key:str = ""
  column_span:int = 1
  row_span:int = 1
  align:str = tkinter.W

  @classmethod
  def from_param (cls, param:IUI|tuple[IUI, int]|tuple[IUI, int, int]|tuple[IUI, int, int, str]|None) -> "typing.Self":
    if isinstance(param, IUI):
      return cls(param)
    elif isinstance(param, tuple):
      match len(param):
        case 2:
          ui, key = param
          return cls(ui, key)
        case 3:
          ui, key, column_span = param
          return cls(ui, key, column_span)
        case 4:
          ui, key, column_span, row_span = param
          return cls(ui, key, column_span, row_span)
        case 5:
          ui, key, column_span, row_span, align = param
          return cls(ui, key, column_span, row_span, align)
        case 6:
          ui, key, column_span, row_span, align = param
          return cls(ui, key, column_span, row_span, align)
        case _:
          raise ValueError(param) #tmp.
    elif param is None:
      return cls(None)
    else:
      raise ValueError(param) #tmp.

class UI_Layout (IUI):

  """グリッドレイアウトを実現します。
  """

  def __init__ (
    self, 
    uis:list[list[IUI|tuple[IUI, str]|tuple[IUI, str, int]|tuple[IUI, str, int, int]|tuple[IUI, str, int, int, str]|None]], 
    as_single_value:bool=False):

    """インスタンスの初期化を行います。

    Parameters
    ----------
    uis : list[list[IUI|tuple[IUI, str]|tuple[IUI, str, int]|tuple[IUI, str, int, int]|tuple[IUI, str, int, int, str]|None]]
      ウィジットの配置を指示するための2次元配列形式のリストです。
    as_single_value : bool
      本引数が有効ならば get_value メソッドの返り値を辞書ではなく単体の値にします。
      本引数が未指定ならば False が設定されます。
    """

    self.uis = uis
    self.as_single_value = as_single_value

  @property
  def _cell_infos (self) -> list[list[_CellInfo]]:
    return [
      [
        _CellInfo.from_param(ui) for ui in inner_uis
      ] for inner_uis in self.uis
    ]

  def get_value (self) -> "dict[str, typing.Any]|typing.Any":
    if self.as_single_value:
      for inner_cell_infos in self._cell_infos:
        for cell_info in inner_cell_infos:
          if cell_info.ui and cell_info.key:
            return cell_info.ui.get_value()
      else:
        return None
    else:
      result = {}
      for inner_cell_infos in self._cell_infos:
        for cell_info in inner_cell_infos:
          if cell_info.ui and cell_info.key:
            result[cell_info.key] = cell_info.ui.get_value()
      return result

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":
    base_frame = tkinter.ttk.Frame(master)
    row = 0
    for inner_cell_infos in self._cell_infos:
      if row == 0:
        pady = 0
      else:
        pady = (const_.PADDING, 0)
      column = 0
      for cell_info in inner_cell_infos:
        if column == 0:
          padx = 0
        else:
          padx = (const_.PADDING, 0)
        if cell_info.ui:
          built = cell_info.ui.build(base_frame)
          built.grid(
            column=column, 
            columnspan=cell_info.column_span, 
            row=row, 
            rowspan=cell_info.row_span, 
            sticky=cell_info.align,
            padx=padx, 
            pady=pady
          )
        column += cell_info.column_span
      row += min((ci.row_span for ci in inner_cell_infos), default=0)
    return base_frame

  def load_from_param (self, param:"list[typing.Any]"):
    if isinstance(param, list):
      uis = [cinfo.ui for cinfo in itertools.chain.from_iterable(self._cell_infos) if cinfo.ui]
      for ui, ui_param in zip(uis, param):
        ui.load_from_param(ui_param)
    else:
      raise ValueError(param) #tmp.
  
  def save_as_param (self) -> "list[typing.Any]":
    uis = [cinfo.ui for cinfo in itertools.chain.from_iterable(self._cell_infos) if cinfo.ui]
    param = [ui.save_as_param() for ui in uis]
    return param
