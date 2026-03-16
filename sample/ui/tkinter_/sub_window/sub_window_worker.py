
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

def update_func () -> bool:
  global should_repeat_var
  global should_raise_error_var
  if should_raise_error_var.get():
    print("Update: Should raise error!")
    raise Exception()
  else:
    print("Update!")
    time.sleep(1)
    return not should_repeat_var.get()

def failed_func ():
  print("Failed!")

def succeed_func ():
  print("Succeed!")

def widget_update_func ():
  print("Widget update!")

def widget_failed_func ():
  print("Widget failed!")

def widget_succeed_func ():
  print("Widget succeed!")

def on_pressed ():
  global tk
  global is_modal_var
  global pause_on_asking_var
  global ask_on_closing_var
  modal = uilib.ui.tkinter_.sub_window.SubWindow_Worker(
    tk, 
    setup_func,
    update_func=update_func,
    failed_func=failed_func,
    succeed_func=succeed_func,
    widget_update_func=widget_update_func,
    widget_failed_func=widget_failed_func,
    widget_succeed_func=widget_succeed_func,
    is_modal=is_modal_var.get(),
    pause_on_asking=pause_on_asking_var.get(),
    ask_on_closing=ask_on_closing_var.get()
  )

tk = tkinter.Tk()
tk.title("Sample window")
base_frame = tkinter.ttk.Frame(tk)
base_frame.pack(
  padx=uilib.const_.PADDING_L, 
  pady=uilib.const_.PADDING_L
)
should_repeat_var = tkinter.IntVar(value=0)
should_repeat_checkbutton = tkinter.ttk.Checkbutton(base_frame, text="shoud repeat?", variable=should_repeat_var)
should_repeat_checkbutton.pack()
should_raise_error_var = tkinter.IntVar(value=0)
should_raise_error_checkbutton = tkinter.ttk.Checkbutton(base_frame, text="shoud raise error?", variable=should_raise_error_var)
should_raise_error_checkbutton.pack(pady=(uilib.const_.PADDING, 0))
is_modal_var = tkinter.IntVar(value=0)
is_modal_checkbutton = tkinter.ttk.Checkbutton(base_frame, text="is modal?", variable=is_modal_var)
is_modal_checkbutton.pack(pady=(uilib.const_.PADDING, 0))
pause_on_asking_var = tkinter.IntVar(value=0)
pause_on_asking_checkbutton = tkinter.ttk.Checkbutton(base_frame, text="pause on asking?", variable=pause_on_asking_var)
pause_on_asking_checkbutton.pack(pady=(uilib.const_.PADDING, 0))
ask_on_closing_var = tkinter.IntVar(value=0)
ask_on_closing_checkbutton = tkinter.ttk.Checkbutton(base_frame, text="ask on closing?", variable=ask_on_closing_var)
ask_on_closing_checkbutton.pack(pady=(uilib.const_.PADDING, 0))
button = tkinter.ttk.Button(base_frame, text="Start", command=on_pressed)
button.pack(pady=(uilib.const_.PADDING_L, 0))
tk.mainloop()
