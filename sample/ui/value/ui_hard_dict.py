
import uilib
import tkinter
import tkinter.ttk

tk = tkinter.Tk()
tk.title("Sample window")
tk.minsize(320, 240)
ui = uilib.ui.value.UI_HardDict(
  {
    "name": uilib.ui.value.UI_Str("abc"),
    "age": uilib.ui.value.UI_Int(12, (0, 100, 1))
  },
  {
    "name": "名前",
    "age": "年齢"
  }
)
ui.build(tk).pack(padx=10, pady=10)
button = tkinter.ttk.Button(tk, text="Print", command=lambda: print(repr(ui.get_value())))
button.pack(padx=10, pady=(0, 10))
tk.mainloop()
