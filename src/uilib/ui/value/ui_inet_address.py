
import tkinter
import tkinter.ttk
from uilib import const_
from uilib import global_
from uilib import language
from uilib.ui.abc import IUI
from uilib.ui.value.ui_str import UI_Str
from uilib.ui.value.ui_number import UI_Int

"""
+------+---------+
| host | entry   |
+------+---------+
| port | spinbox |
+------+---------+
"""

class UI_InetAddress (IUI):

  def _on_changed (self):
    if self.callback:
      self.callback(self.get_value())

  def _callback (self, value:"typing.Any"):
    self._on_changed()

  def __init__ (
    self,
    address:tuple[str, int],
    *,
    language:dict[str, str]|None=None,
    readonly:bool=False,
    callback:"typing.Callable[[tuple[str, int]], None]|None"=None):
    self.language = language or global_.DEFAULT_LANGUAGE
    self.callback = callback
    host, port = address
    self.ui_host = UI_Str(host, readonly=readonly, callback=self._callback)
    self.ui_port = UI_Int(port, (0, 65535, 1), readonly=readonly, callback=self._callback)

  def get_value (self) -> tuple[str, int]:
    return (
      self.ui_host.get_value(),
      self.ui_port.get_value(),
    )

  def build (self, master:tkinter.Widget) -> tkinter.Widget:
    base_frame = tkinter.ttk.Frame(master)
    base_frame.columnconfigure(1, weight=1)
    host_label = tkinter.ttk.Label(base_frame, text=language.translate("LABEL_INET_ADDRESS_HOST", self.language))
    host_label.grid(column=0, row=0, sticky=tkinter.NE)
    self.ui_host.build(base_frame).grid(column=1, row=0, sticky=tkinter.W)
    port_label = tkinter.ttk.Label(base_frame, text=language.translate("LABEL_INET_ADDRESS_PORT", self.language))
    port_label.grid(column=0, row=1, sticky=tkinter.NE, pady=(const_.PADDING, 0))
    self.ui_port.build(base_frame).grid(column=1, row=1, sticky=tkinter.W, pady=(const_.PADDING, 0))
    return base_frame

  def load_from_param (self, param:"dict[str, typing.Any]"):
    if isinstance(param, dict):
      self.ui_host.load_from_param(param["host"])
      self.ui_port.load_from_param(param["port"])
      self._on_changed()
    else:
      raise ValueError(param) #tmp.
  
  def save_as_param (self) -> "dict[str, typing.Any]":
    return {
      "host": self.ui_host.save_as_param(),
      "port": self.ui_port.save_as_param(),
    }
