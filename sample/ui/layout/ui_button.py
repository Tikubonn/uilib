
import uilib
import tkinter

tk = tkinter.Tk()
tk.title("Sample window")
tk.geometry("640x480")
ui_button = uilib.ui.layout.UI_Button("Say hello", lambda: print("Hello!"))
ui_button.build(tk).pack(padx=10, pady=10)
button = tkinter.Button(tk, text="Print", command=lambda: print(repr(ui_button.get_value())))
button.pack(padx=10, pady=(0, 10))
tk.mainloop()
