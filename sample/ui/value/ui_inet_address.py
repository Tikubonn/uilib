
import uilib
import tkinter
import tkinter.ttk

def callback (value:tuple[str, int]):
  print("Changed to", value)

def pressed_on_print ():
  global ui
  global ui_readonly
  print(repr(ui.get_value()))
  print(repr(ui_readonly.get_value()))

tk = tkinter.Tk()
ui = uilib.ui.value.UI_InetAddress(("127.0.0.1", 8080), callback=callback)
ui.build(tk).pack(padx=10, pady=(10, 0))
ui_readonly = uilib.ui.value.UI_InetAddress(("127.0.0.1", 8080), readonly=True, callback=callback)
ui_readonly.build(tk).pack(padx=10, pady=(10, 0))
button = tkinter.ttk.Button(tk, text="Print", command=pressed_on_print)
button.pack(padx=10, pady=10)
tk.mainloop()
