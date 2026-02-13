
import tkinter
import tkinter.ttk

class Scrollable (tkinter.ttk.Frame):

  """縦スクロール可能なTkinterウィジットを実現します。"""

  def _build (self, widget_factory_func:"typing.Callable[[tkinter.Widget], tkinter.Widget]"):
    self.columnconfigure(0, weight=1)
    widget = widget_factory_func(self)
    widget.grid(column=0, row=0, sticky=tkinter.EW)
    scrollbar = tkinter.Scrollbar(self, orient=tkinter.VERTICAL)
    scrollbar.grid(column=1, row=0, sticky=tkinter.NS)
    scrollbar.config(command=widget.yview)
    widget.config(yscrollcommand=scrollbar.set)
    self._widget = widget
  
  def __init__ (self, master:tkinter.Widget, widget_factory_func:"typing.Callable[[tkinter.Widget], tkinter.Widget]"):
    super().__init__(master)
    self._widget = None
    self._build(widget_factory_func)

  @property
  def widget (self) -> tkinter.Widget:
    return self._widget
