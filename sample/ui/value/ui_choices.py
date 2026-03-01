
import uilib
import tkinter
import tkinter.ttk

def callback (value:int):
  print("Changed to", repr(value))

tk = tkinter.Tk()
tk.title("Sample window")
tk.minsize(320, 240)
ui = uilib.ui.value.UI_Choices(
  1,
  [1,2,3],
  callback=callback
)
ui.build(tk).pack(padx=10, pady=10)
button = tkinter.ttk.Button(tk, text="Print", command=lambda: print(repr(ui.get_value())))
button.pack(padx=10, pady=(0, 10))
tk.mainloop()
