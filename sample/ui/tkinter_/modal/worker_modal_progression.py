
import time
import uilib
import tkinter
import tkinter.ttk

def progression_func (worker_state:uilib.ui.tkinter_.modal.WorkerModal):
  TOTAL_COUNT = 100
  sum_ = 0
  for i in range(TOTAL_COUNT +1):
    match worker_state.status:
      case uilib.ui.tkinter_.modal.WorkerStatus.PENDING:
        sum_ += i
        worker_state.set_progression(i / TOTAL_COUNT)
        time.sleep(1 / TOTAL_COUNT)
      case _:
        break
  worker_state.set_result(sum_)

def completed_func (result:int):
  print("Result is", result)

def on_pressed ():
  global tk
  modal = uilib.ui.tkinter_.modal.WorkerModal_Progression(
    tk,
    "Sample modal", 
    "Calculate sum numbers between 0 ~ 100.",
    progression_func,
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
