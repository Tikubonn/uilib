
import time
import uilib
import tkinter
import tkinter.ttk
from dataclasses import dataclass

@dataclass
class SleepFor:

  duration:int

  def __call__ (self) -> int:
    time.sleep(self.duration)
    print(self.duration) #test.
    return self.duration

def completed_func (result:int):
  print("Result is", result, "Sum is", sum(result))

def on_pressed ():
  global tk
  modal = uilib.ui.tkinter_.modal.WorkerModal_ThreadingProgression(
    tk,
    "Sample modal", 
    "Calculate sum numbers between 0 ~ 100.",
    [SleepFor(i) for i in range(10)],
    completed_func
  )

tk = tkinter.Tk()
tk.title("Sample window")
button = tkinter.ttk.Button(tk, text="Start", command=on_pressed)
button.pack(
  padx=uilib.const_.PADDING_L, 
  pady=uilib.const_.PADDING_L
)
tk.mainloop()
