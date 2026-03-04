
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

def update_func ():
  print("Update!")
  time.sleep(1)

def exit_func ():
  print("Exit!")

def on_pressed ():
  global tk
  modal = uilib.ui.tkinter_.sub_window.SubWindow_Worker(
    tk, 
    setup_func,
    update_func,
    exit_func
  )

tk = tkinter.Tk()
tk.title("Sample window")
button = tkinter.ttk.Button(tk, text="Start", command=on_pressed)
button.pack(
  padx=uilib.const_.PADDING_L, 
  pady=uilib.const_.PADDING_L
)
tk.mainloop()
