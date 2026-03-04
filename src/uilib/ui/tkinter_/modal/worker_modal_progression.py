
import tkinter
import tkinter.ttk
from .worker_modal import WorkerModal

class WorkerModal_Progression (WorkerModal):

  _MAX_PROGRESSION_VALUE:"typing.ClassVar[int]" = 1000

  def _update_progression_text (self):
    iprogression = self.progression_var.get()
    self.progression_text_var.set("{:>6.1f}%".format(iprogression / self._MAX_PROGRESSION_VALUE * 100.0))

  def _setup_func (self, master:tkinter.Widget):
    base_frame = tkinter.ttk.Frame(master)
    base_frame.pack(padx=12, pady=12)
    message_label = tkinter.ttk.Label(
      base_frame, 
      text=self.message, 
      justify=tkinter.CENTER
    )
    message_label.pack(fill=tkinter.X, expand=True)
    progression_frame = tkinter.ttk.Frame(base_frame)
    progression_frame.pack(fill=tkinter.X, expand=True, pady=(12, 0))
    progression_label = tkinter.ttk.Label(
      progression_frame, 
      textvariable=self.progression_text_var,
      justify=tkinter.RIGHT
    )
    progression_label.grid(column=0, row=1)
    progression_bar = tkinter.ttk.Progressbar(
      progression_frame, 
      variable=self.progression_var, 
      maximum=self._MAX_PROGRESSION_VALUE,
      orient=tkinter.HORIZONTAL
    )
    progression_bar.grid(column=1, row=1, sticky=tkinter.EW, padx=(4, 0))
    self._update_progression_text()

  def _update_func (self, progression:float):
    iprogression = int(progression * self._MAX_PROGRESSION_VALUE)
    self.progression_var.set(iprogression)
    self._update_progression_text()

  def __init__ (
    self, 
    master:"tkinter.Widget",
    title:str, 
    message:str,
    progression_func:"typing.Callable[[uilib.ui.tkinter_.modal.worker_modal.WorkerState], None]",
    completion_func:"typing.Callable[[typing.Any], None]|None"=None,
    *,
    language:dict[str, str]|None=None):
    self.message = message
    self.progression_var = tkinter.IntVar(value=0)
    self.progression_text_var = tkinter.StringVar(value="")
    super().__init__(
      master, 
      self._setup_func, 
      self._update_func,
      progression_func,
      completion_func,
      language=language
    )
    self.title(title)
