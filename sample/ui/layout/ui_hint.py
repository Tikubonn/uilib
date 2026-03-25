
import uilib
import tkinter
import tkinter.ttk

tk = tkinter.Tk()
ui = uilib.ui.layout.UI_Hint("This is tooltip text.")
ui.build(tk).pack(padx=10, pady=10)
button_frame = tkinter.ttk.Frame(tk)
button_frame.pack(fill=tkinter.X, padx=10, pady=10)
print_as_param_button = tkinter.ttk.Button(
  button_frame, 
  text="Print as param", 
  command=lambda: print(repr(ui.save_as_param()))
)
print_as_param_button.pack(side=tkinter.RIGHT)
print_button = tkinter.ttk.Button(
  button_frame, 
  text="Print value", 
  command=lambda: print(repr(ui.get_value()))
)
print_button.pack(side=tkinter.RIGHT)
tk.mainloop()
