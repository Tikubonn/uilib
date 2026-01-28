
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

def test_ui_bool (tk):
  ui_bool = uilib.ui.value.UI_Bool(False)
  built = ui_bool.build(tk)
  built.pack(fill=tkinter.X)
  assert ui_bool.get_value() == False
  ui_bool.load_from_param(True)
  assert ui_bool.get_value() == True
  with pytest.raises(ValueError):
    ui_bool.load_from_param(None)
