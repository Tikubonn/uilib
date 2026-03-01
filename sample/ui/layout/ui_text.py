
import uilib
import tkinter
import tkinter.ttk

tk = tkinter.Tk()
tk.title("Sample window")
tk.geometry("640x480")
ui_text = uilib.ui.layout.UI_Text("This is sample text.\nThis is sample text.\nThis is sample text.")
ui_text.build(tk).pack(fill=tkinter.X, padx=10, pady=10)
button_frame = tkinter.ttk.Frame(tk)
button_frame.pack(fill=tkinter.X, padx=10, pady=10)
print_as_param_button = tkinter.ttk.Button(
  button_frame, 
  text="Print as param", 
  command=lambda: print(repr(ui_text.save_as_param()))
)
print_as_param_button.pack(side=tkinter.RIGHT)
print_button = tkinter.ttk.Button(
  button_frame, 
  text="Print value", 
  command=lambda: print(repr(ui_text.get_value()))
)
print_button.pack(side=tkinter.RIGHT)
tk.mainloop()
