
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

def test_ui_toggle (tk):
  ui_toggle = uilib.ui.layout.UI_Toggle(
    uilib.ui.value.UI_Int(123)
  )
  built = ui_toggle.build(tk)
  built.pack()
  assert ui_toggle.get_value() == 123
  ui_toggle.load_from_param(456)
  assert ui_toggle.get_value() == 456
