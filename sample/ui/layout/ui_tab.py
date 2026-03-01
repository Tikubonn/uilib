
import uilib
import tkinter
import tkinter.ttk

tk = tkinter.Tk()
tk.title("Sample window")
tk.geometry("640x480")
ui_tab = uilib.ui.layout.UI_Tab([
  ("abc", uilib.ui.value.UI_Int(0, (0, 100, 1))),
  ("def", uilib.ui.value.UI_Int(1, (0, 100, 1))),
  ("ghi", uilib.ui.value.UI_Int(2, (0, 100, 1))),
])
ui_tab.build(tk).pack(fill=tkinter.X)
button_frame = tkinter.ttk.Frame(tk)
button_frame.pack(fill=tkinter.X, padx=10, pady=10)
print_as_param_button = tkinter.ttk.Button(
  button_frame, 
  text="Print as param", 
  command=lambda: print(repr(ui_tab.save_as_param()))
)
print_as_param_button.pack(side=tkinter.RIGHT)
print_button = tkinter.ttk.Button(
  button_frame, 
  text="Print value", 
  command=lambda: print(repr(ui_tab.get_value()))
)
print_button.pack(side=tkinter.RIGHT)
tk.mainloop()
