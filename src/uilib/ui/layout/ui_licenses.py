
import tkinter
import tkinter.ttk
import tkinter.scrolledtext
import itertools
from uilib import const_
from uilib.ui.abc import IUI
from uilib.ui.value.ui_str import UI_Str
from uilib.ui.value.ui_dict import UI_Dict
from uilib.ui.value.ui_hard_dict import UI_HardDict
from collections import OrderedDict
from dataclasses import dataclass, field

@dataclass
class License:

  product:str
  license:str
  additional_infos:list[tuple[str, str]]=field(default_factory=list)

class _UI_License (IUI):

  def __init__ (self, license:"License"):
    self.license = license

  def get_value (self) -> None:
    return None

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":
    base_frame = tkinter.ttk.Frame(master)
    label_product = tkinter.ttk.Label(
      base_frame, 
      text=self.license.product
    )
    label_product.pack(fill=tkinter.X)
    add_info_uis = [
      (key, UI_Str(content, readonly=True)) for key, content in self.license.additional_infos
    ]
    if add_info_uis:
      add_info_dict = UI_HardDict(add_info_uis)
      add_info_dict_built = add_info_dict.build(base_frame)
      add_info_dict_built.pack(
        fill=tkinter.X, 
        pady=(const_.PADDING_L, 0)
      )
    text = tkinter.scrolledtext.ScrolledText(base_frame, state=tkinter.NORMAL)
    text.insert(tkinter.END, self.license.license)
    text.config(state=tkinter.DISABLED)
    text.pack(fill=tkinter.X, pady=(const_.PADDING_L, 0))
    return base_frame

  def load_from_param (self, param:None):
    if param is None:
      pass
    else:
      raise ValueError("Given an invalid param: {!r}".format(param))

  def save_as_param (self) -> None:
    return None

class UI_Licenses (IUI):

  def __init__ (self, licenses:"list[License]"):
    self.licenses = licenses

    ui_licenses = OrderedDict()
    for license in licenses:
      for count in itertools.count():
        if 0 < count:
          product_key = "{:s}({:d})".format(license.product, count +1)
        else:
          product_key = license.product
        if product_key not in ui_licenses:
          ui_licenses[product_key] = _UI_License(license)
          break

    self.ui = UI_Dict(ui_licenses, readonly=True)

  def get_value (self) -> None:
    return None

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":
    return self.ui.build(master)

  def load_from_param (self, param:None):
    if param is None:
      pass
    else:
      raise ValueError("Given an invalid param: {!r}".format(param))

  def save_as_param (self) -> None:
    return None
