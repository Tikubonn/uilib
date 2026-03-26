
import logging
import tkinter
import tkinter.ttk
from uilib import const_
from uilib import image_set
from uilib.ui.abc import IUI
from dataclasses import dataclass

_LOGGER:"logging.Logger" = logging.getLogger(__name__)

"""
+-----------------+--------+
|                 | add    |
+----+------+-----+--------+
| up | down | ... | delete |
+----+------+-----+--------+
| up | down | ... | delete |
+----+------+-----+--------+
| up | down | ... | delete |
+----+------+-----+--------+
"""

@dataclass
class _HandlerSet:

  index:int
  ui_list:"uilib.ui.value.ui_list.UI_List"

  def move_up (self):
    self.ui_list.move_up(self.index)

  def move_down (self):
    self.ui_list.move_down(self.index)

  def delete (self):
    self.ui_list.delete(self.index)

class UI_List (IUI):

  """任意長のリストを表現する UI を提供します。
  """

  def __init__ (
    self, 
    initial_uis:"list[uilib.ui.abc.IUI]", 
    *,
    add_func:"typing.Callable[[], uilib.ui.abc.IUI]|None"=None, 
    callback:"typing.Callable[[list[typing.Any]], None]|None"=None,
    readonly:bool=False):

    """インスタンスの初期化を行います。

    Parameters
    ----------
    initial_uis : list[uilib.ui.abc.IUI]
      初期値として表示される UI のリストです。
    add_func : typing.Callable[[], uilib.ui.abc.IUI]|None
      要素追加時に実行される UI の作成関数です。
      未指定ならば None が設定され、追加ボタンが無効化されます。
    callback : typing.Callable[[list[typing.Any]], None]|None
      要素の並びもしくは要素数が変更されたときに呼び出される関数です。
      未指定ならば None が設定されます。
    readonly : bool
      本引数が真であれば全要素の並び替えと削除、そして新たな要素を追加できないようにします。
      ただし、これらの制限は表示されるウィジットにのみ適用されます。
    """

    self.uis = initial_uis
    self.add_func = add_func
    self.callback = callback
    self.readonly = readonly
    self.content_outer_frame = None
    self.content_frame = None
    self.icon_add = None
    self.icon_move_up = None
    self.icon_move_down = None
    self.icon_delete = None

  def _can_move_up (self, index:int) -> bool:

    """指定要素を1つ上に移動できるかどうかを判定します。

    Notes
    -----
    本関数は判定に際して self.readonly の状態を考慮しません。

    Parameters
    ----------
    index : int
      判定する要素の添え字です。

    Returns
    -------
    bool
      移動可能であるかを表現する真偽値です。
    """

    return 0 < index and index < len(self.uis)

  def _on_changed (self):
    if self.callback:
      self.callback(self.get_value())

  def move_up (self, index:int):
    if self._can_move_up(index):
      ui1 = self.uis[index]
      ui2 = self.uis[index -1]
      self.uis[index] = ui2
      self.uis[index -1] = ui1 
      self._rebuild()
      self._on_changed()
    else:
      raise IndexError(index)

  def _can_move_down (self, index:int) -> bool:

    """指定要素を1つ下に移動できるかどうかを判定します。

    Notes
    -----
    本関数は判定に際して self.readonly の状態を考慮しません。

    Parameters
    ----------
    index : int
      判定する要素の添え字です。

    Returns
    -------
    bool
      移動可能であるかを表現する真偽値です。
    """

    return 0 <= index and index +1 < len(self.uis)

  def move_down (self, index:int):
    if self._can_move_down(index):
      ui1 = self.uis[index]
      ui2 = self.uis[index +1]
      self.uis[index] = ui2 
      self.uis[index +1] = ui1 
      self._rebuild()
      self._on_changed()
    else:
      raise IndexError(index)

  def delete (self, index:int):
    if 0 <= index and index < len(self.uis):
      self.uis = self.uis[:index] + self.uis[index +1:]
      self._rebuild()
      self._on_changed()
    else:
      raise IndexError(index)

  def get_value (self) -> "list[typing.Any]":
    return [ui.get_value() for ui in self.uis]

  def _build_content_frame (self, master:"tkinter.Widget") -> "tkinter.Widget":
    content_frame = tkinter.ttk.Frame(master)
    content_frame.columnconfigure(2, weight=1)
    for i, ui in enumerate(self.uis):

      #separator.

      separator_v = tkinter.ttk.Separator(
        content_frame, 
        orient=tkinter.HORIZONTAL
      )
      separator_v.grid(column=0, columnspan=4, row=i * 2, sticky=tkinter.EW, pady=const_.PADDING)
      handler_set = _HandlerSet(i, self)

      #up button.

      if not self.readonly and self._can_move_up(i): #self.readonly=True ならば常に tkinter.DISABLED.
        up_button_state = tkinter.NORMAL
      else:
        up_button_state = tkinter.DISABLED
      up_button = tkinter.ttk.Button(
        content_frame, 
        image=self.icon_move_up,
        command=handler_set.move_up, 
        state=up_button_state
      )
      up_button.grid(column=0, row=i * 2 + 1, sticky=tkinter.N)

      #down button.

      if not self.readonly and self._can_move_down(i): #self.readonly=True ならば常に tkinter.DISABLED.
        down_button_state = tkinter.NORMAL
      else:
        down_button_state = tkinter.DISABLED
      down_button = tkinter.ttk.Button(
        content_frame, 
        image=self.icon_move_down,
        command=handler_set.move_down, 
        state=down_button_state
      )
      down_button.grid(column=1, row=i * 2 + 1, sticky=tkinter.N)

      #ui.

      built = ui.build(content_frame)
      built.grid(column=2, row=i * 2 + 1, padx=const_.PADDING_L)

      #delete button.

      if self.readonly:
        delete_button_state = tkinter.DISABLED
      else:
        delete_button_state = tkinter.NORMAL
      delete_button = tkinter.ttk.Button(
        content_frame, 
        image=self.icon_delete,
        command=handler_set.delete,
        state=delete_button_state,
      )
      delete_button.grid(column=3, row=i * 2 + 1, sticky=tkinter.N)
    return content_frame

  def _rebuild (self):
    if self.content_outer_frame:
      content_frame = self._build_content_frame(self.content_outer_frame)
      content_frame.pack(fill=tkinter.X)
      self.content_frame.destroy()
      self.content_frame = content_frame

  def _on_pressed_add (self):
    if self.add_func:
      ui = self.add_func()
      self.uis.append(ui)
      self._rebuild()
    else:

      _LOGGER.debug("Pressed add button, but .add_func is None: {!r}".format(self)) #log.

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":

    #Load icons.

    self.icon_add = image_set.get_image("image/icon/add.png", (12, 12))
    self.icon_move_up = image_set.get_image("image/icon/move-up.png", (12, 12))
    self.icon_move_down = image_set.get_image("image/icon/move-down.png", (12, 12))
    self.icon_delete = image_set.get_image("image/icon/delete.png", (12, 12))

    #main.

    base_frame = tkinter.ttk.Frame(master, relief=tkinter.GROOVE)
    inner_frame = tkinter.ttk.Frame(base_frame)
    inner_frame.pack(fill=tkinter.X, padx=const_.PADDING_L, pady=const_.PADDING_L)
    button_frame = tkinter.ttk.Frame(inner_frame)
    button_frame.pack(fill=tkinter.X)

    #add button.

    if self.readonly and self.add_func:
      add_button_state = tkinter.DISABLED
    else:
      add_button_state = tkinter.NORMAL
    add_button = tkinter.ttk.Button(
      button_frame, 
      image=self.icon_add,
      command=self._on_pressed_add,
      state=add_button_state
    )
    add_button.pack(side=tkinter.RIGHT)

    #...

    content_frame = self._build_content_frame(inner_frame)
    content_frame.pack(fill=tkinter.X)
    self.content_outer_frame = inner_frame
    self.content_frame = content_frame
    return base_frame

  def load_from_param (self, param:"list[typing.Any]"):
    if isinstance(param, list):
      self.uis.clear()
      for inner_param in param:
        ui = self.add_func()
        ui.load_from_param(inner_param)
        self.uis.append(ui)
      self._rebuild()
      self._on_changed()
    else:
      raise ValueError(param) #tmp.
  
  def save_as_param (self) -> "list[typing.Any]":
    return [ui.save_as_param() for ui in self.uis]
