
import uilib
import tkinter
import tkinter.ttk

tk = tkinter.Tk()
ui = uilib.ui.value.UI_List(
  [uilib.ui.value.UI_Int(i, (0, 100, 1)) for i in range(3)], 
  add_func=lambda: uilib.ui.value.UI_Int(0, (0, 100, 1))
)
ui.build(tk).pack(padx=10, pady=(10, 0))
ui2 = uilib.ui.value.UI_List(
  [uilib.ui.value.UI_Int(i, (0, 100, 1)) for i in range(3)], 
  readonly=True
)
ui2.build(tk).pack(padx=10, pady=(10, 0))
button = tkinter.ttk.Button(tk, text="Print", command=lambda: print(repr(ui.get_value()), repr(ui2.get_value())))
button.pack(padx=10, pady=10)
tk.mainloop()
