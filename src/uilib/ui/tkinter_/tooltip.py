
import tkinter
import tkinter.ttk
from uilib import const_

class TooltipOverlay (tkinter.Toplevel):

  def _build (self):
    base_frame = tkinter.ttk.Frame(self)
    base_frame.pack()
    label = tkinter.ttk.Label(base_frame, text=self.text)
    label.pack(fill=tkinter.X, padx=const_.PADDING, pady=const_.PADDING)

  def __init__ (self, master:"tkinter.Widget", text:str):
    super().__init__(master)
    self.wm_overrideredirect(True)
    self.text = text
    self._build()

class Tooltip:

  _OFFSET:"typing.ClassVar[tuple[int, int]]" = (12, 12)

  def _overlay_update (self, position:tuple[int, int]):
    if self.overlay:
      x, y = position
      off_x, off_y = self._OFFSET
      self.overlay.geometry("+{:d}+{:d}".format(x + off_x, y + off_y))

  def _on_enter (self, event:"tkinter.Event"):
    if not self.overlay:
      self.overlay = TooltipOverlay(self.widget, self.text)
      self._overlay_update((event.x_root, event.y_root))

  def _on_motion (self, event:"tkinter.Event"):
    if self.overlay:
      self._overlay_update((event.x_root, event.y_root))

  def _on_leave (self, event:"tkinter.Event"):
    if self.overlay:
      self.overlay.destroy()
      self.overlay = None

  def _setup (self):
    self.widget.bind("<Enter>", self._on_enter)
    self.widget.bind("<Motion>", self._on_motion)
    self.widget.bind("<Leave>", self._on_leave)

  def __init__ (self, widget:"tkinter.Widget", text:str):
    self.widget = widget
    self.text = text
    self.overlay = None
    self._setup()
