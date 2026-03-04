
import uilib
import tkinter
import tkinter.ttk

def setup_func (master:tkinter.Widget):
  master.title("Sample modal")
  label = tkinter.ttk.Label(master, text="This is sample text.")
  label.pack(
    padx=uilib.const_.PADDING_L, 
    pady=uilib.const_.PADDING_L
  )

def on_pressed ():
  global tk
  modal = uilib.ui.tkinter_.modal.Modal(tk, setup_func)

tk = tkinter.Tk()
tk.title("Sample window")
button = tkinter.ttk.Button(tk, text="Start", command=on_pressed)
button.pack(
  padx=uilib.const_.PADDING_L, 
  pady=uilib.const_.PADDING_L
)
tk.mainloop()
