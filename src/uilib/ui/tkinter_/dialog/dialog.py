
import tkinter

class Dialog (tkinter.Toplevel):

  def __init__ (
    self, 
    master:"tkinter.Widget", 
    setup_func:"typing.Callable[[tkinter.Widget], None]"):
    super().__init__(master)
    setup_func(self)
    self.transient(master)
    self.grab_set()
