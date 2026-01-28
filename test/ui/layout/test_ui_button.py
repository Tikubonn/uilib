
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

def test_ui_button (tk):
  ui_button = uilib.ui.layout.UI_Button("abc", lambda: None)
  built = ui_button.build(tk)
  built.pack()
  assert ui_button.get_value() is None
  ui_button.load_from_param(123)
  assert ui_button.get_value() is None
