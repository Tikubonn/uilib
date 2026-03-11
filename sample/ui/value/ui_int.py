
import uilib
import tkinter
import tkinter.ttk

def callback (value:int):
  print("Changed to", value)

def pressed_on_print ():
  global ui
  global ui2
  global ui2_readonly
  print(repr(ui.get_value()))
  print(repr(ui2.get_value()))
  print(repr(ui2_readonly.get_value()))

tk = tkinter.Tk()
ui = uilib.ui.value.UI_Int(1, callback=callback)
ui.build(tk).pack(anchor=tkinter.W, padx=10, pady=(10, 0))
ui2 = uilib.ui.value.UI_Int(2, (0, 100, 1), callback=callback)
ui2.build(tk).pack(anchor=tkinter.W, padx=10, pady=(10, 0))
ui2_readonly = uilib.ui.value.UI_Int(2, (0, 100, 1), readonly=True, callback=callback)
ui2_readonly.build(tk).pack(anchor=tkinter.W, padx=10, pady=(10, 0))
button = tkinter.ttk.Button(tk, text="Print", command=pressed_on_print)
button.pack(padx=10, pady=10)
tk.mainloop()
