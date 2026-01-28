
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

def test_ui_str (tk):
  ui_str = uilib.ui.value.UI_Str("abc")
  built = ui_str.build(tk)
  built.pack(fill=tkinter.X)
  assert ui_str.get_value() == "abc"
  ui_str.load_from_param("def")
  assert ui_str.get_value() == "def"
  with pytest.raises(ValueError):
    ui_str.load_from_param(None)
