
import uilib
import pytest
import tkinter
from enum import Flag, auto, unique

@unique
class SampleFlag (Flag):

  A = auto()
  B = auto()
  C = auto()

def test_ui_flag (test_toplevel):
  ui_flag = uilib.ui.value.UI_Flag(SampleFlag.A, SampleFlag)
  built = ui_flag.build(test_toplevel)
  built.pack(fill=tkinter.X)
  assert ui_flag.get_value() is SampleFlag.A
  assert ui_flag.save_as_param() == [SampleFlag.A.name]
  ui_flag.load_from_param([SampleFlag.A.name, SampleFlag.B.name])
  assert ui_flag.get_value() is SampleFlag.A|SampleFlag.B
  assert ui_flag.save_as_param() == [SampleFlag.A.name, SampleFlag.B.name]
  with pytest.raises(ValueError):
    ui_flag.load_from_param(None)

def test_ui_flag_readonly (test_toplevel):
  ui_flag = uilib.ui.value.UI_Flag(SampleFlag.A, SampleFlag, readonly=True)
  built = ui_flag.build(test_toplevel)
  built.pack(fill=tkinter.X)
  assert ui_flag.get_value() is SampleFlag.A
  assert ui_flag.save_as_param() == [SampleFlag.A.name]
  ui_flag.load_from_param([SampleFlag.A.name, SampleFlag.B.name])
  assert ui_flag.get_value() is SampleFlag.A
  assert ui_flag.save_as_param() == [SampleFlag.A.name]
