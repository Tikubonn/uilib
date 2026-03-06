
import tkinter
import tkinter.ttk
import itertools
from uilib import const_
from typing import Generator
from .sub_window_worker import SubWindow_Worker, WorkerStatus

class SubWindow_WorkerProgression (SubWindow_Worker):

  _MAX_PROGRESSION_VALUE:"typing.ClassVar[int]" = 1000

  def __update_progression_text (self):
    progression_int = self.__progression_var.get()
    self.__progression_label_var.set("{:>5.1f}%".format(progression_int / self._MAX_PROGRESSION_VALUE * 100.0))

  def __setup_func (self, master:"tkinter.Toplevel"):
    master.title(self.__title)
    base_frame = tkinter.ttk.Frame(master)
    base_frame.pack(padx=const_.PADDING_L, pady=const_.PADDING_L)
    message_label = tkinter.ttk.Label(base_frame, text=self.__message)
    message_label.grid(column=0, columnspan=2, row=0, sticky=tkinter.EW)
    progression_label = tkinter.ttk.Label(base_frame, textvariable=self.__progression_label_var)
    progression_label.grid(column=0, row=1, sticky=tkinter.E, pady=(const_.PADDING_L, 0))
    progression_bar = tkinter.ttk.Progressbar(base_frame, orient=tkinter.HORIZONTAL, variable=self.__progression_var, maximum=self._MAX_PROGRESSION_VALUE)
    progression_bar.grid(column=1, row=1, sticky=tkinter.EW, pady=(const_.PADDING_L, 0), padx=(const_.PADDING, 0))
    self.__update_progression_text()

  def _set_progression (self, progression:float):
    self.__cur_progression = max(self.__cur_progression, min(1.0, progression))

  def __wrapped_update_func (self):
    progressions = self.__update_func()
    if isinstance(progressions, Generator):
      progressions = itertools.chain(progressions, (1.0,))
      while True:
        match self._worker_status:
          case WorkerStatus.PENDING:
            try:
              progression = next(progressions)
              self._set_progression(progression)
            except StopIteration:
              break
          case WorkerStatus.PAUSED:
            pass
          case WorkerStatus.FAILED | WorkerStatus.SUCCEED:
            break
          case _:
            raise ValueError(self._worker_status)
      return True #Don't repeat again.
    else:
      raise ValueError(progressions)

  def __widget_update_func (self):
    progression_int = round(self.__cur_progression * self._MAX_PROGRESSION_VALUE)
    self.__progression_var.set(progression_int)
    self.__update_progression_text()

  def __init__ (
    self,
    master:"tkinter.Widget",
    title:str,
    message:str,
    *,
    update_func:"typing.Callable[[], typing.Generator[float, None, None]]|None",
    failed_func:"typing.Callable[[], None]|None"=None,
    succeed_func:"typing.Callable[[], None]|None"=None,
    widget_failed_func:"typing.Callable[[], None]|None"=None,
    widget_succeed_func:"typing.Callable[[], None]|None"=None,
    language:"dict[str, str]|None"=None,
    is_modal:bool=False,
    pause_on_asking:bool=False):
    self.__title = title
    self.__message = message
    self.__update_func = update_func
    self.__progression_var = tkinter.IntVar(value=0)
    self.__progression_label_var = tkinter.StringVar(value="")
    self.__cur_progression = 0.0
    super().__init__(
      master,
      self.__setup_func,
      update_func=self.__wrapped_update_func,
      failed_func=failed_func,
      succeed_func=succeed_func,
      widget_update_func=self.__widget_update_func,
      widget_failed_func=widget_failed_func,
      widget_succeed_func=widget_succeed_func,
      language=language,
      is_modal=is_modal,
      pause_on_asking=pause_on_asking
    )
