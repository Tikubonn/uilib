
import uilib
import tkinter

tk = tkinter.Tk()
tk.title("Sample window")
tk.geometry("640x480")

str_var = tkinter.StringVar(value="abc")
int_var = tkinter.IntVar(value=123)

def build_func (master:"tkinter.Widget") -> "tkinter.Widget":
  frame = tkinter.Frame(master)
  str_entry = tkinter.Entry(frame, textvariable=str_var)
  str_entry.pack()
  int_entry = tkinter.Entry(frame, textvariable=int_var)
  int_entry.pack(pady=(10, 0))
  return frame

def load_func (param):
  str_value, int_value = param
  str_var.set(str_value)
  int_var.set(int_value)

ui_user_def = uilib.ui.layout.UI_UserDef(
  build_func=build_func,
  load_func=load_func,
  value_func=lambda: [str_var.get(), int_var.get()]
)
ui_user_def.build(tk).pack(padx=10, pady=10)

button = tkinter.Button(tk, text="Print", command=lambda: print(repr(ui_user_def.get_value())))
button.pack(padx=10, pady=(0, 10))

tk.mainloop()
