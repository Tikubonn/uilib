
import uilib
import tkinter
import tkinter.ttk

tk = tkinter.Tk()
ui = uilib.ui.value.UI_List([], add_func=lambda: uilib.ui.value.UI_Int(0, (0, 100, 1)))
ui.build(tk).pack(padx=10, pady=(10, 0))
button = tkinter.ttk.Button(tk, text="Print", command=lambda: print(repr(ui.get_value())))
button.pack(padx=10, pady=10)
tk.mainloop()
