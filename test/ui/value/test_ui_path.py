
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

def test_ui_path (tk):
  ui_path = uilib.ui.value.UI_Path("abc")
  built = ui_path.build(tk)
  built.pack(fill=tkinter.X)
  assert ui_path.get_value() == "abc"
  ui_path.load_from_param("def")
  assert ui_path.get_value() == "def"
  with pytest.raises(ValueError):
    ui_path.load_from_param(None)
