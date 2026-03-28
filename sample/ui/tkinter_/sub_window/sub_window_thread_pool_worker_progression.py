
import time
import uilib
import tkinter
import tkinter.ttk
from dataclasses import dataclass

@dataclass(frozen=True)
class Sleep:

  duration:int

  def __call__ (self):
    global should_raise_error_var
    if should_raise_error_var.get():
      raise ValueError()
    else:
      for i in range(self.duration):
        print("Update: {:d}/{:d}".format(i + 1, self.duration))
        yield (i + 1) / self.duration
        time.sleep(1)

def failed_func (exception:Exception|None):
  print("Failed: {!r}".format(exception))

def succeed_func ():
  print("Succeed!")

def widget_failed_func (exception:Exception|None):
  print("Widget failed: {!r}".format(exception))

def widget_succeed_func ():
  print("Widget succeed!")

def on_pressed ():
  global tk
  global is_modal_var
  global pause_on_asking_var
  global ask_on_closing_var
  modal = uilib.ui.tkinter_.sub_window.SubWindow_ThreadPoolWorkerProgression(
    tk, 
    "Sample title",
    "Sample message",
    update_funcs=[Sleep(i) for i in range(3, 6)],
    failed_func=failed_func,
    succeed_func=succeed_func,
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
should_raise_error_var = tkinter.IntVar(value=0)
should_raise_error_checkbutton = tkinter.ttk.Checkbutton(base_frame, text="shoud raise error?", variable=should_raise_error_var)
should_raise_error_checkbutton.pack()
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
