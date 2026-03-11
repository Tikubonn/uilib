
import logging
import tkinter
import tkinter.ttk
import tkinter.filedialog
from enum import Enum, auto, unique
from uilib import const_
from uilib import image_set
from uilib.ui.abc import IUI

_LOGGER:logging.Logger = logging.getLogger(__name__)

@unique
class PathType (Enum):

  FILE = auto()
  DIRECTORY = auto()

class UI_Path (IUI):

  """ファイルパスを表現する UI を提供します。
  """

  def __init__ (
    self, 
    value:str, 
    type_:PathType,
    *,
    file_types:list[tuple[str, str]]=[],
    readonly:bool=False,
    callback:"typing.Callable[[str], None]|None"=None):

    """インスタンスの初期化を行います。

    Parameters
    ----------
    value : str
      初期値となる任意のパス名です。
      指定するパスがない場合には空文字列を指定することができます。
    type_ : PathType
      取得するパスの種類を表す PathType 列挙型です。
    file_types : list[tuple[str, str]]
      ファイル選択ダイアログで選択されるファイルの種類を指定します。
      例えば `[("テキストファイル", "*.txt")]` 等の値を指定することができます。
      本引数は type_ 引数に PathType.FILE が指定された場合のみ有効です。
      本引数が未指定の場合、空リストが設定されます。
    callback : typing.Callable[[str], None]|None
      UI の値が変更された際に実行される関数です。
      本引数が未指定の場合 None が設定されます。
    """

    self.str_var = tkinter.StringVar(value=value)
    self.type = type_
    self.file_types = file_types
    self.readonly = readonly
    self.callback = callback
    self.icon_search = None
    self.icon_delete = None

  def get_value (self) -> str:
    return self.str_var.get()

  def _on_changed (self):
    if self.callback:
      self.callback(self.get_value())

  def _on_pressed_search (self):
    match self.type:
      case PathType.FILE:
        path = tkinter.filedialog.askopenfilename(filetypes=self.file_types)
      case PathType.DIRECTORY:
        path = tkinter.filedialog.askdirectory()
      case _:
        raise ValueError(self.type) #tmp.
    if path:
      self.str_var.set(path)
      self._on_changed()

  def _on_pressed_delete (self):
    self.str_var.set("")
    self._on_changed()

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":

    #Load icons.

    self.icon_search = image_set.get_image("image/icon/search.png", (12, 12))
    self.icon_delete = image_set.get_image("image/icon/delete.png", (12, 12))

    #Main

    base_frame = tkinter.ttk.Frame(master)
    base_frame.columnconfigure(0, weight=1)
    entry = tkinter.ttk.Entry(
      base_frame, 
      textvariable=self.str_var, 
      state=tkinter.DISABLED,
      width=const_.TEXT_FORM_WIDTH
    )
    entry.grid(column=0, row=0, sticky=tkinter.EW)
    if self.readonly:
      button_state = tkinter.DISABLED
    else:
      button_state = tkinter.NORMAL
    search_button = tkinter.ttk.Button(
      base_frame, 
      image=self.icon_search, 
      command=self._on_pressed_search,
      state=button_state
    )
    search_button.grid(column=1, row=0, padx=(const_.PADDING, 0))
    delete_button = tkinter.ttk.Button(
      base_frame,
      image=self.icon_delete,
      command=self._on_pressed_delete,
      state=button_state
    )
    delete_button.grid(column=2, row=0)
    return base_frame

  def load_from_param (self, param:str):
    if isinstance(param, str):
      if not self.readonly:
        self.str_var.set(param)
        self._on_changed()
      else:

        _LOGGER.debug("Ignored loading param because instance is readonly: {!r} <- {!r}".format(self, param)) #log.
        
    else:
      raise ValueError(param) #tmp.
  
  def save_as_param (self) -> str:
    return self.str_var.get()
