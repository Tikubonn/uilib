
import tkinter
import tkinter.ttk
import tkinter.messagebox
from uilib import const_
from uilib import image_set
from uilib.ui.abc import IUI
from collections import OrderedDict

"""
+-------+-----+-----+--------+---------+
| entry | add | set | delete | content |
+-------+-----+-----+--------+         |
| list                       |         |
|                            |         |
|                            |         |
+----------------------------+---------+
"""

class _ScrollableListbox (tkinter.Frame):

  def _setup_widget (self, *args, **kwargs):
    self.grid_columnconfigure(0, weight=1)
    listbox = tkinter.Listbox(self, *args, **kwargs)
    listbox.grid(column=0, row=0, sticky=tkinter.EW)
    scrollbar = tkinter.Scrollbar(self)
    scrollbar.grid(column=1, row=0, sticky=tkinter.NS)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)
    self.listbox = listbox
    self.scrollbar = scrollbar

  def __init__ (self, master:tkinter.Widget, *args, **kwargs):
    super().__init__(master)
    self.scrollbar = None
    self.listbox = None
    self._setup_widget(*args, **kwargs)

class UI_Dict (IUI):

  """文字列をキーとする辞書を表現する uilib.ui.abc.IUI オブジェクトです。"""

  def __init__ (self, uis:"dict[str, uilib.ui.abc.IUI]", add_func:"typing.Callable[[], uilib.ui.abc.IUI]"):
    self.uis = OrderedDict(uis)
    self.add_func = add_func
    self.entry_var = tkinter.StringVar(value="")
    self.listbox_var = tkinter.StringVar(value="")
    self.base_frame = None
    self.content_frame = None
    self.scrollable_listbox = None

  def get_value (self) -> "dict[str, uilib.ui.abc.IUI]":
    return {key: ui.get_value() for key, ui in self.uis.items()}

  def _update_listbox_var (self):
    value = tuple(self.uis.keys())
    self.listbox_var.set(value)

  def _update_content_frame (self):
    curselection = self.scrollable_listbox.listbox.curselection()
    if curselection:
      index, = curselection
      key = self.scrollable_listbox.listbox.get(index)
      ui = self.uis[key]
      self.content_frame.destroy()
      content_frame = tkinter.Frame(self.base_frame)
      content_frame.grid(column=5, row=0, rowspan=2, sticky=tkinter.NW, padx=const_.PADDING, pady=const_.PADDING)
      built = ui.build(content_frame)
      built.pack(fill=tkinter.BOTH, expand=True)
      self.content_frame = content_frame
    else:
      self.content_frame.destroy()
      content_frame = tkinter.Frame(self.base_frame)
      content_frame.grid(column=5, row=0, rowspan=2, sticky=tkinter.NW, padx=const_.PADDING, pady=const_.PADDING)
      self.content_frame = content_frame

  def _on_add (self):
    key = self.entry_var.get()
    if key:
      if key not in self.uis:
        ui = self.add_func()
        self.uis[key] = ui
        self._update_listbox_var()
        self._update_content_frame()
      else:
        # raise KeyError(key)
        tkinter.messagebox.showerror("Key Error", "New key has been already exists.")
    else:
      # raise ValueError()
      tkinter.messagebox.showerror("Key Error", "Key is an empty str.")

  def _on_set (self):
    key = self.entry_var.get()
    if key:
      if key not in self.uis:
        curselection = self.scrollable_listbox.listbox.curselection()
        if curselection:
          answer = tkinter.messagebox.askokcancel("Change?", "Do you really want to change it?")
          if answer:
            index, = curselection
            old_key = self.scrollable_listbox.listbox.get(index)
            self.uis = OrderedDict((((key if k == old_key else k), ui) for k, ui in self.uis.items()))
            self._update_listbox_var()
            self._update_content_frame()
        else:
          raise ValueError()
      else:
        # raise KeyError(key)
        tkinter.messagebox.showerror("Key Error", "Key has been already exists.")
    else:
      # raise ValueError()
      tkinter.messagebox.showerror("Key Error", "Key is an empty str.")

  def _on_delete (self):
    key = self.entry_var.get()
    if key:
      if key in self.uis:
        answer = tkinter.messagebox.askokcancel("Delete?", "Do you really want to delete it?")
        if answer:
          self.uis.pop(key)
          self._update_listbox_var()
          self._update_content_frame()
      else:
        # raise KeyError(key)
        tkinter.messagebox.showerror("Key Error", "Key has been not exists.")
    else:
      # raise ValueError()
      tkinter.messagebox.showerror("Key Error", "Key is an empty str.")

  def _on_select (self, event:tkinter.Widget):
    curselection = self.scrollable_listbox.listbox.curselection()
    if curselection:
      index, = curselection
      key = self.scrollable_listbox.listbox.get(index)
      self.entry_var.set(key)
      self._update_content_frame()
    else:

      # tkinter の選択範囲は全てのウィジットで共通だと推察されます。
      # そのため tkinter.Entry で範囲選択が行われると tkinter.Listbox の選択状態が自動的に解消されてしまいます。
      # 論理的には self.entry_var に空文字列を設定するのが望ましいのですが、直観に反するため元文字列を維持するように処理します。

      # self.entry_var.set("")
      # self._update_content_frame()
      pass

  def build (self, master:"tkinter.Widget") -> "tkinter.Widget":
    base_frame = tkinter.Frame(master, bd=2, relief=tkinter.GROOVE)
    entry = tkinter.Entry(base_frame, textvariable=self.entry_var)
    entry.grid(column=0, row=0, sticky=tkinter.EW, padx=const_.PADDING, pady=const_.PADDING, ipady=const_.INNER_PADDING)
    add_button = tkinter.Button(base_frame, image=image_set.get_image("icon-add", (16, 16)), command=self._on_add)
    add_button.grid(column=1, row=0, sticky=tkinter.NS, padx=const_.PADDING, pady=const_.PADDING, ipadx=const_.INNER_PADDING)
    set_button = tkinter.Button(base_frame, image=image_set.get_image("icon-edit", (16, 16)), command=self._on_set)
    set_button.grid(column=2, row=0, sticky=tkinter.NS, padx=const_.PADDING, pady=const_.PADDING, ipadx=const_.INNER_PADDING)
    delete_button = tkinter.Button(base_frame, image=image_set.get_image("icon-delete", (16, 16)), command=self._on_delete)
    delete_button.grid(column=3, row=0, sticky=tkinter.NS, padx=const_.PADDING, pady=const_.PADDING, ipadx=const_.INNER_PADDING)
    scrollable_listbox = _ScrollableListbox(base_frame, listvariable=self.listbox_var)
    scrollable_listbox.grid(column=0, columnspan=4, row=1, sticky=tkinter.NSEW, padx=const_.PADDING, pady=const_.PADDING)
    scrollable_listbox.listbox.bind("<<ListboxSelect>>", self._on_select)
    separator_v = tkinter.ttk.Separator(base_frame, orient=tkinter.VERTICAL)
    separator_v.grid(column=4, row=0, rowspan=2, sticky=tkinter.NS, padx=const_.PADDING)
    content_frame = tkinter.Frame(base_frame)    
    content_frame.grid(column=5, row=0, rowspan=2, sticky=tkinter.NW, padx=const_.PADDING, pady=const_.PADDING)
    self.base_frame = base_frame
    self.content_frame = content_frame
    self.scrollable_listbox = scrollable_listbox
    self._update_listbox_var()
    self._update_content_frame()
    return base_frame

  def load_from_param (self, param:"dict[str, typing.Any]"):
    if isinstance(param, dict):
      self.uis.clear()
      for key, inner_param in param.items():
        ui = self.add_func()
        ui.load_from_param(inner_param)
        self.uis[key] = ui
      self._update_listbox_var()
      self._update_content_frame()
    else:
      raise ValueError(param) #tmp.
