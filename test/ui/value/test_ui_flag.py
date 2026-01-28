
import time
import uilib
import pytest
import tkinter
from enum import Flag, auto, unique

@pytest.fixture
def tk () -> tkinter.Tk:
  tk = tkinter.Tk()
  yield tk
  tk.destroy()
  time.sleep(1)

@unique
class SampleFlag (Flag):

  A = auto()
  B = auto()
  C = auto()

def test_ui_flag (tk):
  ui_flag = uilib.ui.value.UI_Flag(SampleFlag.A, SampleFlag)
  built = ui_flag.build(tk)
  built.pack(fill=tkinter.X)
  assert ui_flag.get_value() is SampleFlag.A
  ui_flag.load_from_param(SampleFlag.A|SampleFlag.B)
  assert ui_flag.get_value() is SampleFlag.A|SampleFlag.B
  with pytest.raises(ValueError):
    ui_flag.load_from_param(None)
