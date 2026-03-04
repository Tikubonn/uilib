
import time
import uilib
import tkinter
import tkinter.ttk

class WorkerModal_Sample (uilib.ui.tkinter_.modal.WorkerModal):

  def _setup_func (self, master:tkinter.Widget):
    master.title("Sample modal")
    label = tkinter.ttk.Label(master, textvariable=self.label_var)
    label.pack(
      padx=uilib.const_.PADDING_L, 
      pady=uilib.const_.PADDING_L
    )

  def _update_func (self, progression:float):
    self.label_var.set("{:.2f}".format(progression))

  def _progression_func (self, worker_state:uilib.ui.tkinter_.modal.WorkerModal):
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

  def _completed_func (self, result:int):
    print("Result is", result)

  def __init__ (self, master:tkinter.Widget):
    self.label_var = tkinter.StringVar(value="")
    super().__init__(
      master,
      self._setup_func,
      self._update_func,
      self._progression_func,
      self._completed_func
    )

def on_pressed ():
  global tk
  modal = WorkerModal_Sample(tk)

tk = tkinter.Tk()
tk.title("Sample window")
button = tkinter.ttk.Button(tk, text="Start", command=on_pressed)
button.pack(
  padx=uilib.const_.PADDING_L, 
  pady=uilib.const_.PADDING_L
)
tk.mainloop()
