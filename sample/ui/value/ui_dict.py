
import uilib
import logging
import tkinter
import tkinter.ttk

logging.basicConfig(level=logging.DEBUG)

tk = tkinter.Tk()
ui = uilib.ui.value.UI_Dict(
  {"{:d}".format(i): uilib.ui.value.UI_Int(i, (0, 100, 1)) for i in range(3)}, 
  add_func=lambda: uilib.ui.value.UI_Int(0, (0, 100, 1)),
  language={}
)
ui.build(tk).pack(padx=10, pady=(10, 0))
ui2 = uilib.ui.value.UI_Dict(
  {"{:d}".format(i): uilib.ui.value.UI_Int(i, (0, 100, 1)) for i in range(3)}, 
  language={},
  readonly=True
)
ui2.build(tk).pack(padx=10, pady=(10, 0))
button = tkinter.ttk.Button(tk, text="Print", command=lambda: print(repr(ui.get_value()), repr(ui2.get_value())))
button.pack(padx=10, pady=10)
tk.mainloop()
