
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

import tkinter
import tkinter.ttk
from uilib import const_
from uilib import image_set
from uilib.ui.abc import IUI
from dataclasses import dataclass

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

  """任意長のリストを表現する uilib.ui.abc.IUI オブジェクトです。"""

  def __init__ (self, uis:"list[uilib.ui.abc.IUI]", add_func:"typing.Callable[[], uilib.ui.abc.IUI]"):
    self.uis = uis
    self.add_func = add_func
    self.icon_move_up = None
    self.icon_move_down = None
    self.icon_delete = None
    self.base_frame = None
    self.content_frame = None

  def move_up (self, index:int):
    if 0 < index and index < len(self.uis):
      ui1 = self.uis[index]
      ui2 = self.uis[index -1]
      self.uis[index] = ui2
      self.uis[index -1] = ui1 
      self._rebuild()
    else:
      raise IndexError(index)

  def move_down (self, index:int):
    if 0 <= index and index +1 < len(self.uis):
      ui1 = self.uis[index]
      ui2 = self.uis[index +1]
      self.uis[index] = ui2 
      self.uis[index +1] = ui1 
      self._rebuild()
    else:
      raise IndexError(index)

  def delete (self, index:int):
    if 0 <= index and index < len(self.uis):
      self.uis = self.uis[:index] + self.uis[index +1:]
      self._rebuild()
    else:
      raise IndexError(index)

  def get_value (self) -> "list[typing.Any]":
    return [ui.get_value() for ui in self.uis]

  def _build_content_frame (self, master:"tkinter.Widget") -> "tkinter.Widget":
    content_frame = tkinter.Frame(master)
    row = 0
    for i, ui in enumerate(self.uis):
      content_frame.rowconfigure(row, weight=1)
      content_frame.columnconfigure(3, weight=1)
      h_separator = tkinter.ttk.Separator(content_frame, orient=tkinter.HORIZONTAL)
      h_separator.grid(column=0, columnspan=6, row=row, sticky=tkinter.EW)
      row += 1
      handler_set = _HandlerSet(i, self)
      if i == 0:
        up_button_state = tkinter.DISABLED
      else:
        up_button_state = tkinter.NORMAL
      up_button = tkinter.Button(content_frame, image=self.icon_move_up, command=handler_set.move_up, state=up_button_state)
      up_button.grid(column=0, row=row, padx=const_.PADDING, pady=const_.PADDING, ipadx=const_.INNER_PADDING)
      if i + 1 < len(self.uis):
        down_button_state = tkinter.NORMAL
      else:
        down_button_state = tkinter.DISABLED
      down_button = tkinter.Button(content_frame, image=self.icon_move_down, command=handler_set.move_down, state=down_button_state)
      down_button.grid(column=1, row=row, padx=const_.PADDING, pady=const_.PADDING, ipadx=const_.INNER_PADDING)
      v_separator = tkinter.ttk.Separator(content_frame, orient=tkinter.VERTICAL)
      v_separator.grid(column=2, row=row, sticky=tkinter.NS, padx=const_.PADDING)
      built = ui.build(content_frame)
      built.grid(column=3, row=row, sticky=tkinter.W, padx=const_.PADDING, pady=const_.PADDING)
      v_separator2 = tkinter.ttk.Separator(content_frame, orient=tkinter.VERTICAL)
      v_separator2.grid(column=4, row=row, sticky=tkinter.NS, padx=const_.PADDING)
      delete_button = tkinter.Button(content_frame, image=self.icon_delete, command=handler_set.delete)
      delete_button.grid(column=5, row=row, padx=const_.PADDING, pady=const_.PADDING, ipadx=const_.INNER_PADDING)
      row += 1
    return content_frame

  def _rebuild (self):
    if self.base_frame: #tmp.
      content_frame = self._build_content_frame(self.base_frame)
      content_frame.grid(column=0, row=1, sticky=tkinter.E)
      self.content_frame.destroy()
      self.content_frame = content_frame

  def _on_pressed_add (self):
    ui = self.add_func()
    self.uis.append(ui)
    self._rebuild()

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":

    #Load icon images.

    self.icon_move_up = image_set.get_image("icon-move-up", (16, 16))
    self.icon_move_down = image_set.get_image("icon-move-down", (16, 16))
    self.icon_delete = image_set.get_image("icon-delete", (16, 16))

    #Build.

    base_frame = tkinter.Frame(master, bd=2, relief=tkinter.GROOVE)
    base_frame.columnconfigure(0, weight=1)
    add_button = tkinter.Button(base_frame, image=image_set.get_image("icon-add", (16, 16)), command=self._on_pressed_add)
    add_button.grid(column=0, row=0, sticky=tkinter.E, padx=const_.PADDING, pady=const_.PADDING, ipadx=const_.INNER_PADDING)
    content_frame = self._build_content_frame(base_frame)
    content_frame.grid(column=0, row=1, sticky=tkinter.E)
    self.base_frame = base_frame
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
    else:
      raise ValueError(param) #tmp.
  
  def save_as_param (self) -> "list[typing.Any]":
    return [ui.save_as_param() for ui in self.uis]
