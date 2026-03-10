
import uilib
import tkinter
import tkinter.ttk

tk = tkinter.Tk()
tk.title("Sample window")
ui_layout = uilib.ui.layout.UI_Group(
  "Sample ints",
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
button_frame = tkinter.ttk.Frame(tk)
button_frame.pack(fill=tkinter.X, padx=10, pady=10)
print_as_param_button = tkinter.ttk.Button(
  button_frame, 
  text="Print as param", 
  command=lambda: print(repr(ui_layout.save_as_param()))
)
print_as_param_button.pack(side=tkinter.RIGHT)
print_button = tkinter.ttk.Button(
  button_frame, 
  text="Print value", 
  command=lambda: print(repr(ui_layout.get_value()))
)
print_button.pack(side=tkinter.RIGHT)
tk.mainloop()
