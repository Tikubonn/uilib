
import time
import uilib
import pytest
import tkinter

def test_ui_layout (test_tk):
  ints = [uilib.ui.value.UI_Int(i) for i in range(10)]
  ui_layout = uilib.ui.layout.UI_Layout(
    [
      [
        ints[0],
        (ints[1], 2),
      ],
      [
        (ints[2], 2, 2),
      ],
      [
        (ints[3], 2, 2, tkinter.E),
      ],
    ],
    {
      "int0": ints[0], 
      "int1": ints[1], 
      "int2": ints[2], 
      "int3": ints[3]
    }
  )
  built = ui_layout.build(test_tk)
  built.pack()
  assert ui_layout.get_value() == {"int0": 0, "int1": 1, "int2": 2, "int3": 3}
  assert ui_layout.save_as_param() == [0, 1, 2, 3]
  ui_layout.load_from_param([4, 5, 6, 7])
  assert ui_layout.get_value() == {"int0": 4, "int1": 5, "int2": 6, "int3": 7}
  assert ui_layout.save_as_param() == [4, 5, 6, 7]
  with pytest.raises(ValueError):
    ui_layout.load_from_param(None)

def test_ui_layout_single_value (test_tk):
  ui_int = uilib.ui.value.UI_Int(123)
  ui_layout = uilib.ui.layout.UI_Layout(
    [[ui_int]],
    ui_int
  )
  built = ui_layout.build(test_tk)
  built.pack()
  assert ui_layout.get_value() == 123
  assert ui_layout.save_as_param() == [123]
  ui_layout.load_from_param([456])
  assert ui_layout.get_value() == 456
  assert ui_layout.save_as_param() == [456]
