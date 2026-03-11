
import uilib
import tkinter
import tkinter.ttk

tk = tkinter.Tk()
tk.title("Sample window")
tk.geometry("640x480")
ui_nullable = uilib.ui.layout.UI_Toggle(
  uilib.ui.value.UI_HardDict(
    {
      "name": uilib.ui.value.UI_Str(""),
      "age": uilib.ui.value.UI_Int(0),
    },
    label_table={
      "name": "名前",
      "age": "年齢"
    }
  )
)
ui_nullable.build(tk).pack(fill=tkinter.X, padx=10, pady=10)
button_frame = tkinter.ttk.Frame(tk)
button_frame.pack(fill=tkinter.X, padx=10, pady=10)
print_as_param_button = tkinter.ttk.Button(
  button_frame, 
  text="Print as param", 
  command=lambda: print(repr(ui_nullable.save_as_param()))
)
print_as_param_button.pack(side=tkinter.RIGHT)
print_button = tkinter.ttk.Button(
  button_frame, 
  text="Print value", 
  command=lambda: print(repr(ui_nullable.get_value()))
)
print_button.pack(side=tkinter.RIGHT)
tk.mainloop()
