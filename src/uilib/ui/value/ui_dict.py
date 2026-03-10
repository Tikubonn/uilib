
import tkinter
import tkinter.ttk
import tkinter.messagebox
import tkinter.simpledialog
from uilib import const_
from uilib import global_
from uilib import language
from uilib import image_set
from uilib.ui.abc import IUI
from uilib.ui.tkinter_.scrollable import Scrollable
from collections import OrderedDict

"""
+-------+-----+-----+--------+---+---------+
| entry | add | set | delete | | | content |
+-------+-----+-----+--------+ | |         |
| list                       | | |         |
|                            | | |         |
|                            | | |         |
+----------------------------+---+---------+
"""

class UI_Dict (IUI):

  """文字列をキーとする辞書を表現する uilib.ui.abc.IUI オブジェクトです。"""

  def __init__ (
    self, 
    uis:"dict[str, uilib.ui.abc.IUI]", 
    add_func:"typing.Callable[[], uilib.ui.abc.IUI]",
    *,
    language:dict[str, str]|None=None,
    callback:"typing.Callable[[dict[str, typing.Any]], None]|None"=None):
    self.uis = OrderedDict(uis)
    self.add_func = add_func
    self.language = language or global_.DEFAULT_LANGUAGE
    self.callback = callback
    self.entry_var = tkinter.StringVar(value="")
    self.listbox_var = tkinter.StringVar(value="")
    self.content_outer_frame = None
    self.content_frame = None
    self.scrollable_listbox = None
    self.icon_add = None
    self.icon_edit = None
    self.icon_delete = None

  def get_value (self) -> "dict[str, typing.Any]":
    return {
      key: ui.get_value() for key, ui in self.uis.items()
    }

  def _update_listbox_var (self):
    self.listbox_var.set(list(self.uis.keys()))

  def _on_changed (self):
    if self.callback:
      self.callback(self.get_value())

  def _on_pressed_add (self):
    key = tkinter.simpledialog.askstring(
      language.translate("DIALOG_DICT_ADD_TITLE", self.language),
      language.translate("DIALOG_DICT_ADD", self.language),
      initialvalue=self.entry_var.get()
    )
    if key not in self.uis:
      ui = self.add_func()
      self.uis[key] = ui
      self._update_listbox_var()
      self._rebuild()
      self._on_changed()
    else:
      tkinter.messagebox.showerror(
        language.translate("ERROR_DICT_KEY_EXISTS_TITLE", self.language),
        language.translate("ERROR_DICT_KEY_EXISTS", self.language)
      )

  def _on_pressed_rename (self):
    key = self.entry_var.get()
    if key: #入力欄が空でなければダイアログを表示する。
      alt_key = tkinter.simpledialog.askstring(
        language.translate("DIALOG_DICT_RENAME_TITLE", self.language),
        language.translate("DIALOG_DICT_RENAME", self.language),
        initialvalue=self.entry_var.get()
      )
      if alt_key:
        if key != alt_key:
          if alt_key not in self.uis:
            ui = self.uis[key]
            self.uis[alt_key] = ui
            del self.uis[key]
            self.entry_var.set(alt_key) #置換後に入力欄を新しい名前に差し替えます。
            self._update_listbox_var()
            self._rebuild()
            self._on_changed()
          else:
            tkinter.messagebox.showerror(
              language.translate("ERROR_DICT_KEY_NOT_EXISTS_TITLE", self.language),
              language.translate("ERROR_DICT_KEY_NOT_EXISTS", self.language)
            )
        else:
          tkinter.messagebox.showerror(
            language.translate("ERROR_DICT_SAME_KEY_TITLE", self.language),
            language.translate("ERROR_DICT_SAME_KEY", self.language)
          )

  def _on_pressed_delete (self):
    key = self.entry_var.get()
    if key:
      if key in self.uis:
        answer = tkinter.messagebox.askokcancel(
          language.translate("DIALOG_DICT_DELETE_TITLE", self.language),
          language.translate("DIALOG_DICT_DELETE", self.language)
        )
        if answer:
          del self.uis[key]
          self.entry_var.set("") #削除後に入力欄を空にします。
          self._update_listbox_var()
          self._rebuild()
          self._on_changed()
      else:
        tkinter.messagebox.showerror(
          language.translate("ERROR_DICT_KEY_NOT_EXISTS_TITLE", self.language),
          language.translate("ERROR_DICT_KEY_NOT_EXISTS", self.language)
        )

  def _on_listbox_select (self, event:tkinter.Event|None=None):
    curselection = self.scrollable_listbox.widget.curselection()
    if len(curselection) == 1:
      index, = curselection
      key = self.scrollable_listbox.widget.get(index)
      self.entry_var.set(key)
      self._update_listbox_var()
      self._rebuild()
      self._on_changed()

  def _rebuild (self):
    if self.content_frame:
      content_frame = self._build_content_frame(self.content_outer_frame)
      content_frame.pack(fill=tkinter.X)
      self.content_frame.destroy()
      self.content_frame = content_frame

  def _build_content_frame (self, master:tkinter.Widget) -> tkinter.Widget:
    content_frame = tkinter.ttk.Frame(master)
    if self.scrollable_listbox:
      curselection = self.scrollable_listbox.widget.curselection()
      if len(curselection) == 1:
        index, = curselection
        key = self.scrollable_listbox.widget.get(index)
        ui = self.uis.get(key)
        if ui:
          built = ui.build(content_frame)
          built.pack(fill=tkinter.X)
    return content_frame

  def build (self, master:tkinter.Widget) -> tkinter.Widget:

    #Load icons.

    self.icon_add = image_set.get_image("icon-add", (12, 12))
    self.icon_edit = image_set.get_image("icon-edit", (12, 12))
    self.icon_delete = image_set.get_image("icon-delete", (12, 12))

    #Main

    base_frame = tkinter.ttk.Frame(master, relief=tkinter.GROOVE)
    inner_frame = tkinter.ttk.Frame(base_frame)
    inner_frame.pack(fill=tkinter.X, padx=const_.PADDING_L, pady=const_.PADDING_L)
    inner_frame.columnconfigure(0, weight=1)
    entry = tkinter.ttk.Entry(
      inner_frame, 
      textvariable=self.entry_var, 
      state=tkinter.DISABLED,
      width=const_.TEXT_FORM_WIDTH
    )
    entry.grid(column=0, row=0, sticky=tkinter.EW, padx=(0, const_.PADDING))
    add_button = tkinter.ttk.Button(
      inner_frame,
      image=self.icon_add,
      command=self._on_pressed_add
    )
    add_button.grid(column=1, row=0)
    rename_button = tkinter.ttk.Button(
      inner_frame,
      image=self.icon_edit,
      command=self._on_pressed_rename
    )
    rename_button.grid(column=2, row=0)
    delete_button = tkinter.ttk.Button(
      inner_frame,
      image=self.icon_delete,
      command=self._on_pressed_delete
    )
    delete_button.grid(column=3, row=0)
    scrollable_listbox = Scrollable(
      inner_frame, 
      lambda master: tkinter.Listbox(master, listvariable=self.listbox_var)
    )
    scrollable_listbox.grid(column=0, columnspan=4, row=1, sticky=tkinter.EW, pady=(const_.PADDING, 0))
    scrollable_listbox.widget.bind("<<ListboxSelect>>", self._on_listbox_select)
    separator_v = tkinter.ttk.Separator(inner_frame, orient=tkinter.VERTICAL)
    separator_v.grid(column=4, row=0, rowspan=2, sticky=tkinter.NS, padx=(const_.PADDING_L, 0))
    content_outer_frame = tkinter.ttk.Frame(inner_frame)
    content_outer_frame.grid(column=5, row=0, rowspan=2, sticky=tkinter.NW, padx=(const_.PADDING_L, 0))
    content_frame = self._build_content_frame(content_outer_frame)
    content_frame.pack(fill=tkinter.X)
    self.content_outer_frame = content_outer_frame
    self.content_frame = content_frame
    self.scrollable_listbox = scrollable_listbox
    return base_frame

  def load_from_param (self, param:"dict[str, typing.Any]"):
    if isinstance(param, dict):
      self.uis.clear()
      for key, inner_param in param.items():
        ui = self.add_func()
        ui.load_from_param(inner_param)
        self.uis[key] = ui
      self._update_listbox_var()
      self._rebuild()
      self._on_changed()
    else:
      raise ValueError(param) #tmp.

  def save_as_param (self) -> "dict[str, typing.Any]":
    return {
      key: ui.save_as_param() for key, ui in self.uis.items()
    }
