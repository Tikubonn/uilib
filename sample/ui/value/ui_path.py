
import uilib
import tkinter
import tkinter.ttk

def callback (value:str):
  print("Changed to", repr(value))

tk = tkinter.Tk()
tk.title("Sample window")
tk.minsize(320, 240)
ui_file = uilib.ui.value.UI_Path("", uilib.ui.value.PathType.FILE, callback=callback)
ui_file.build(tk).pack(padx=10, pady=(10, 0))
ui_dir = uilib.ui.value.UI_Path("", uilib.ui.value.PathType.DIRECTORY, callback=callback)
ui_dir.build(tk).pack(padx=10, pady=(10, 0))
button = tkinter.ttk.Button(tk, text="Print", command=lambda: print("file: {!r}, dir: {!r}".format(ui_file.get_value(), ui_dir.get_value())))
button.pack(padx=10, pady=(10, 10))
tk.mainloop()
