
import tkinter

class SubWindow (tkinter.Toplevel):

  def __init__ (
    self,
    master:"tkinter.Widget",
    setup_func:"typing.Callable[[tkinter.Toplevel], None]",
    *,
    is_modal:bool):
    super().__init__(master)
    setup_func(self)
    self.transient(master)
    if is_modal:
      self.grab_set()
