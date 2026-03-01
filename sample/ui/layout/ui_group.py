
import uilib
import tkinter
import tkinter.ttk

tk = tkinter.Tk()
tk.title("Sample window")
tk.geometry("640x480")
ints = [uilib.ui.value.UI_Int(i, (0, 100, 1)) for i in range(9)]
ui_layout = uilib.ui.layout.UI_Group(
  "Int values",
  [
    [ints[0], ints[1], ints[2]], 
    [(ints[3], 2), (ints[4], 1)], 
    [(ints[5], 3, 1, tkinter.E)]], 
  {
    "int0": ints[0],
    "int1": ints[1],
    "int2": ints[2],
    "int3": ints[3],
    "int4": ints[4],
    "int5": ints[5],
  }
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
