
import uilib
import tkinter
import tkinter.ttk

def callback (value:tuple[str, int]):
  print("Changed to", value)

tk = tkinter.Tk()
tk.title("Sample window")
tk.minsize(320, 240)
ui = uilib.ui.value.UI_InetAddress(
  ("127.0.0.1", 8080), 
  callback=callback
)
ui.build(tk).pack(padx=10, pady=10)
button = tkinter.ttk.Button(tk, text="Print", command=lambda: print(repr(ui.get_value())))
button.pack(padx=10, pady=(0, 10))
tk.mainloop()
