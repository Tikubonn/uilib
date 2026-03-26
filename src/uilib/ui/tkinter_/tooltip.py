
import tkinter
import tkinter.ttk
from uilib import const_

class _TooltipOverlay (tkinter.Toplevel):

  """Tooltip インスタンスが作成するツールチップを模したサブウィンドウです。
  """

  _MAX_WIDTH:"typing.ClassVar[int]" = 240

  def _build (self):
    base_frame = tkinter.ttk.Frame(self, borderwidth=1, relief="raised") #視認性のために境界線を表示する
    base_frame.pack()
    message = tkinter.Message(base_frame, text=self.text, width=self._MAX_WIDTH)
    message.pack() #Message 自体にマージンが設定されているため padx, pady は指定しない

  def __init__ (self, master:"tkinter.Widget", text:str):

    """インスタンスの初期化を行います。

    Parameters
    ----------
    widget : tkinter.Widget
      親となるウィジットです。
    text : str
      本サブウィンドウに表示されるテキストです。
    """

    super().__init__(master)
    self.wm_overrideredirect(True)
    self.text = text
    self._build()

class Tooltip:

  """指定要素にマウスオーバーした際にテキストをポップアップする機能を提供します。

  Notes
  -----
  <Motion> イベントを捕捉するために本クラスはウィジットではなく、対象ウィジットを引数に取る独立クラスとして実装されています。
  """

  _OFFSET:"typing.ClassVar[tuple[int, int]]" = (12, 12)

  def _overlay_update (self, position:tuple[int, int]):
    if self.overlay:
      x, y = position
      off_x, off_y = self._OFFSET
      self.overlay.geometry("+{:d}+{:d}".format(x + off_x, y + off_y))

  def _on_enter (self, event:"tkinter.Event"):
    if not self.overlay:
      self.overlay = _TooltipOverlay(self.widget, self.text)
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

    """インスタンスの初期化を行います。

    Warnings
    --------
    引数 widget にこれらのイベントが既に指定されていた場合、本インスタンスはそれらを自身の関数で上書きします。

    * <Enter>
    * <Motion>
    * <Leave>

    Parameters
    ----------
    widget : tkinter.Widget
      ツールチップ機能を追加するウィジットです。
    text : str
      マウスオーバー時に表示されるテキストです。
    """

    self.widget = widget
    self.text = text
    self.overlay = None
    self._setup()
