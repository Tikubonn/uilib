
import uilib
import tkinter

tk = tkinter.Tk()
tk.title("Sample window")
tk.geometry("640x480")
ui_text = uilib.ui.layout.UI_Text("This is sample text.\nThis is sample text.\nThis is sample text.")
ui_text.build(tk).pack(fill=tkinter.X, padx=10, pady=10)
button = tkinter.Button(tk, text="Print", command=lambda: print(repr(ui_text.get_value())))
button.pack(padx=10, pady=(0, 10))
tk.mainloop()
