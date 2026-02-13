
import time
import uilib
import pytest
import tkinter

def test_scrollable (test_tk):
  scrollable = uilib.ui.tkinter_.Scrollable(test_tk, lambda master: tkinter.Listbox(master))
  scrollable.pack(fill=tkinter.X)
  assert isinstance(scrollable.widget, tkinter.Listbox)
