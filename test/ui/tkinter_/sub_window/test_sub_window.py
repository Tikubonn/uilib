
import pytest
import tkinter
import tkinter.ttk
from uilib.ui.tkinter_.sub_window import SubWindow

def test_sub_window (test_toplevel:"tkinter.Toplevel"):

  #最低限の動作確認を行います。

  def setup_func (master:"tkinter.Toplevel"):
    label = tkinter.ttk.Label(master, text="Sample label")
    label.pack()

  sub_window = SubWindow(
    test_toplevel,
    setup_func,
    is_modal=False
  )
  sub_window.destroy()
