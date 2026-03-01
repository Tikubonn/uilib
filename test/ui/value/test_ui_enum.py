
import uilib
import pytest
import tkinter
from enum import Enum, auto, unique

@unique
class SampleEnum (Enum):

  A = auto()
  B = auto()
  C = auto()

def test_ui_enum (test_toplevel):
  ui_enum = uilib.ui.value.UI_Enum(SampleEnum.A, SampleEnum)
  built = ui_enum.build(test_toplevel)
  built.pack(fill=tkinter.X)
  assert ui_enum.get_value() is SampleEnum.A
  assert ui_enum.save_as_param() is SampleEnum.A.name
  ui_enum.load_from_param(SampleEnum.B.name)
  assert ui_enum.get_value() is SampleEnum.B
  assert ui_enum.save_as_param() is SampleEnum.B.name
  with pytest.raises(ValueError):
    ui_enum.load_from_param(None)
