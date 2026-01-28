
import tkinter
import tkinter.ttk
from uilib import const_
from uilib.ui.abc import IUI
from collections import OrderedDict

class UI_HardDict (IUI):

  def __init__ (self, uis:"dict[str, uilib.ui.abc.IUI]", label_table:dict[str, str]={}):
    self.uis = OrderedDict(uis)
    self.label_table = label_table
    self.base_frame = None
    self.content_frame = None

  def get_value (self) -> "dict[str, uilib.ui.abc.IUI]":
    return {k: ui.get_value() for k, ui in self.uis.items()}

  def _build_content (self, master:"tkinter.Widget") -> "tkinter.Widget":
    content_frame = tkinter.Frame(master)
    row = 0
    for key, ui in self.uis.items():
      content_frame.columnconfigure(2, weight=1)
      if 0 < row:
        v_separator = tkinter.ttk.Separator(content_frame, orient=tkinter.HORIZONTAL)
        v_separator.grid(column=0, columnspan=3, row=row, sticky=tkinter.EW)
        row += 1
      label_text = self.label_table.get(key, key)
      label = tkinter.Label(content_frame, text=label_text)
      label.grid(column=0, row=row, padx=const_.PADDING, pady=const_.PADDING)
      h_separator = tkinter.ttk.Separator(content_frame, orient=tkinter.VERTICAL)
      h_separator.grid(column=1, row=row, sticky=tkinter.NS, padx=const_.PADDING)
      built = ui.build(content_frame)
      built.grid(column=2, row=row, sticky=tkinter.W, padx=const_.PADDING, pady=const_.PADDING)
      row += 1
    return content_frame

  def _rebuild (self):
    if self.base_frame: #tmp.
      content_frame = self._build_content(self.base_frame)
      content_frame.pack(fill=tkinter.X)
      self.content_frame.destroy()
      self.content_frame = content_frame

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":
    base_frame = tkinter.Frame(master, bd=2, relief=tkinter.GROOVE)
    content_frame = self._build_content(base_frame)
    content_frame.pack(fill=tkinter.X)
    self.base_frame = base_frame
    self.content_frame = content_frame
    return base_frame

  def load_from_param (self, param:"dict[str, uilib.ui.abc.IUI]"):
    if isinstance(param, dict):
      for key, inner_param in param.items():
        if key in self.uis:
          self.uis[key].load_from_param(inner_param)
        else:
          raise KeyError(key) #tmp.
      self._rebuild()
    else:
      raise ValueError(param) #tmp.
