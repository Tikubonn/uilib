
import uilib
import tkinter
import tkinter.ttk

tk = tkinter.Tk()
tk.title("Sample window")
ui_layout = uilib.ui.layout.UI_Layout(
  [
    [
      (uilib.ui.value.UI_Int(0), "int0"),
      (uilib.ui.value.UI_Int(1), "int1"),
      (uilib.ui.value.UI_Int(2), "int2"),
    ],
    [
      (uilib.ui.value.UI_Int(3), "int3", 2),
      (uilib.ui.value.UI_Int(4), "int4"),
    ],
    [
      (uilib.ui.value.UI_Int(5), "int5", 3, 1, tkinter.E)
    ]
  ]
)
ui_layout.build(tk).pack(padx=10, pady=10)
button = tkinter.ttk.Button(tk, text="Print", command=lambda: print(repr(ui_layout.get_value())))
button.pack(padx=10, pady=(0, 10))
tk.mainloop()
