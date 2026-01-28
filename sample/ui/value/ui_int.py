
import uilib
import tkinter

tk = tkinter.Tk()
tk.title("Sample window")
tk.minsize(320, 240)
ui = uilib.ui.value.UI_Int(1)
ui.build(tk).pack(anchor=tkinter.W, padx=10, pady=10)
ui2 = uilib.ui.value.UI_Int(2, (0, 100, 1))
ui2.build(tk).pack(anchor=tkinter.W, padx=10, pady=(0, 10))
button = tkinter.Button(tk, text="Print", command=lambda: print(repr(ui.get_value()), repr(ui2.get_value())))
button.pack(padx=10, pady=(0, 10))
tk.mainloop()
