
import uilib
import tkinter

tk = tkinter.Tk()
tk.title("Sample window")
tk.minsize(320, 240)
ui = uilib.ui.value.UI_List([], add_func=lambda: uilib.ui.value.UI_Int(0, (0, 100, 1)))
ui.build(tk).pack(padx=10, pady=10)
button = tkinter.Button(tk, text="Print", command=lambda: print(repr(ui.get_value())))
button.pack(padx=10, pady=(0, 10))
tk.mainloop()
