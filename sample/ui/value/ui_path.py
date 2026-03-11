
import uilib
import tkinter
import tkinter.ttk

def callback (value:str):
  print("Changed to", repr(value))

def pressed_on_print ():
  global ui_file
  global ui_dir
  global ui_file_readonly
  global ui_dir_readonly
  print(repr(ui_file.get_value()))
  print(repr(ui_dir.get_value()))
  print(repr(ui_file_readonly.get_value()))
  print(repr(ui_dir_readonly.get_value()))

tk = tkinter.Tk()
ui_file = uilib.ui.value.UI_Path("", uilib.ui.value.PathType.FILE, callback=callback)
ui_file.build(tk).pack(padx=10, pady=(10, 0))
ui_dir = uilib.ui.value.UI_Path("", uilib.ui.value.PathType.DIRECTORY, callback=callback)
ui_dir.build(tk).pack(padx=10, pady=(10, 0))
ui_file_readonly = uilib.ui.value.UI_Path("", uilib.ui.value.PathType.FILE, readonly=True, callback=callback)
ui_file_readonly.build(tk).pack(padx=10, pady=(10, 0))
ui_dir_readonly = uilib.ui.value.UI_Path("", uilib.ui.value.PathType.DIRECTORY, readonly=True, callback=callback)
ui_dir_readonly.build(tk).pack(padx=10, pady=(10, 0))
button = tkinter.ttk.Button(tk, text="Print", command=pressed_on_print)
button.pack(padx=10, pady=(10, 10))
tk.mainloop()
