
import time
import uilib
import pytest
import tkinter
from uilib.ui.value.ui_number import _UI_Number

@pytest.fixture
def tk () -> tkinter.Tk:
  tk = tkinter.Tk()
  yield tk
  tk.destroy()
  time.sleep(1)

def test_ui_number (tk):
  int_var = tkinter.IntVar(value=0)
  ui_number = _UI_Number(int_var)
  built = ui_number.build(tk)
  built.pack(fill=tkinter.X)
  assert ui_number.get_value() == 0
  ui_number.load_from_param(1)
  assert ui_number.get_value() == 1

def test_ui_int (tk):
  ui_int = uilib.ui.value.UI_Int(0)
  built = ui_int.build(tk)
  built.pack(fill=tkinter.X)
  assert ui_int.get_value() == 0
  ui_int.load_from_param(1)
  assert ui_int.get_value() == 1
  with pytest.raises(ValueError):
    ui_int.load_from_param(None)

def test_ui_float (tk):
  ui_float = uilib.ui.value.UI_Float(0.0)
  built = ui_float.build(tk)
  built.pack(fill=tkinter.X)
  assert ui_float.get_value() == 0.0
  ui_float.load_from_param(1.25)
  assert ui_float.get_value() == 1.25
  with pytest.raises(ValueError):
    ui_float.load_from_param(None)
