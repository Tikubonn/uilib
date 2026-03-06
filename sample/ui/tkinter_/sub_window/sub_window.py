
import time
import uilib
import tkinter
import tkinter.ttk

def setup_func (master:"tkinter.Widget"):
  label = tkinter.ttk.Label(master, text="Sample")
  label.pack(
    padx=uilib.const_.PADDING_L, 
    pady=uilib.const_.PADDING_L
  )

def on_pressed ():
  global tk
  global is_modal_var
  modal = uilib.ui.tkinter_.sub_window.SubWindow(
    tk, 
    setup_func, 
    is_modal=is_modal_var.get()
  )

tk = tkinter.Tk()
tk.title("Sample window")
base_frame = tkinter.ttk.Frame(tk)
base_frame.pack(
  padx=uilib.const_.PADDING_L, 
  pady=uilib.const_.PADDING_L
)
is_modal_var = tkinter.IntVar(value=0)
is_modal_checkbutton = tkinter.ttk.Checkbutton(base_frame, text="is modal?", variable=is_modal_var)
is_modal_checkbutton.pack()
button = tkinter.ttk.Button(base_frame, text="Start", command=on_pressed)
button.pack(pady=(uilib.const_.PADDING_L, 0))
tk.mainloop()
