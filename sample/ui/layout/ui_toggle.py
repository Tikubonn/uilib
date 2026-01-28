
import uilib
import tkinter

tk = tkinter.Tk()
tk.title("Sample window")
tk.geometry("640x480")
ui_nullable = uilib.ui.layout.UI_Toggle(
  uilib.ui.value.UI_HardDict(
    {
      "name": uilib.ui.value.UI_Str(""),
      "age": uilib.ui.value.UI_Int(0),
    },
    {
      "name": "名前",
      "age": "年齢"
    }
  )
)
ui_nullable.build(tk).pack(anchor=tkinter.W, padx=10, pady=10)
button = tkinter.Button(tk, text="Print", command=lambda: print(repr(ui_nullable.get_value())))
button.pack(padx=10, pady=(0, 10))
tk.mainloop()
