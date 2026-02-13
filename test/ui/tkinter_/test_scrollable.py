
import time
import uilib
import pytest
import tkinter

@pytest.fixture
def tk () -> tkinter.Tk:
  tk = tkinter.Tk()
  yield tk
  tk.destroy()
  time.sleep(1)

def test_scrollable (tk):
  scrollable = uilib.ui.tkinter_.Scrollable(tk, lambda master: tkinter.Listbox(master))
  scrollable.pack(fill=tkinter.X)
  assert isinstance(scrollable.widget, tkinter.Listbox)
