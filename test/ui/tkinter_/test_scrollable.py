
import uilib
import pytest
import tkinter

def test_scrollable (test_toplevel):
  scrollable = uilib.ui.tkinter_.Scrollable(test_toplevel, lambda master: tkinter.Listbox(master))
  scrollable.pack(fill=tkinter.X)
  assert isinstance(scrollable.widget, tkinter.Listbox)
