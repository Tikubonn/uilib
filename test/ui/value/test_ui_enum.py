
import time
import uilib
import pytest
import tkinter
from enum import Enum, auto, unique

@pytest.fixture
def tk () -> tkinter.Tk:
  tk = tkinter.Tk()
  yield tk
  tk.destroy()
  time.sleep(1)

@unique
class SampleEnum (Enum):

  A = auto()
  B = auto()
  C = auto()

def test_ui_enum (tk):
  ui_enum = uilib.ui.value.UI_Enum(SampleEnum.A, SampleEnum)
  built = ui_enum.build(tk)
  built.pack(fill=tkinter.X)
  assert ui_enum.get_value() is SampleEnum.A
  ui_enum.load_from_param(SampleEnum.B)
  assert ui_enum.get_value() is SampleEnum.B
  with pytest.raises(ValueError):
    ui_enum.load_from_param(None)
