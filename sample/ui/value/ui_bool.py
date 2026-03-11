
import uilib
import tkinter
import tkinter.ttk

def callback (value:bool):
  print("Changed to", value)

def on_pressed_print ():
  global ui
  global ui_readonly
  print(repr(ui.get_value()))
  print(repr(ui_readonly.get_value()))

tk = tkinter.Tk()
ui = uilib.ui.value.UI_Bool(True, callback=callback)
ui.build(tk).pack(padx=10, pady=(10, 0))
ui_readonly = uilib.ui.value.UI_Bool(True, readonly=True, callback=callback)
ui_readonly.build(tk).pack(padx=10, pady=(10, 0))
button = tkinter.ttk.Button(tk, text="Print", command=on_pressed_print)
button.pack(padx=10, pady=10)
tk.mainloop()
