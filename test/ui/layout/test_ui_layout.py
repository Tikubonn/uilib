
import uilib
import pytest
import tkinter

def test_ui_layout (test_toplevel):
  ui_layout = uilib.ui.layout.UI_Layout(
    [
      [
        uilib.ui.value.UI_Int(0),
        (uilib.ui.value.UI_Int(1), "int1"),
      ],
      [
        (uilib.ui.value.UI_Int(2), "int2", 3),
      ],
      [
        (uilib.ui.value.UI_Int(3), "int3", 3, 1),
      ],
      [
        (uilib.ui.value.UI_Int(4), "", 3, 1, tkinter.E),
      ],
    ]
  )
  built = ui_layout.build(test_toplevel)
  built.pack()
  assert ui_layout.get_value() == {"int1": 1, "int2": 2, "int3": 3}
  assert ui_layout.save_as_param() == [0, 1, 2, 3, 4]
  ui_layout.load_from_param([10, 11, 12, 13, 14])
  assert ui_layout.get_value() == {"int1": 11, "int2": 12, "int3": 13}
  assert ui_layout.save_as_param() == [10, 11, 12, 13, 14]
  with pytest.raises(ValueError):
    ui_layout.load_from_param(None)

def test_ui_layout_as_single_value (test_toplevel):
  ui_layout = uilib.ui.layout.UI_Layout(
    [
      [
        uilib.ui.value.UI_Int(0),
        (uilib.ui.value.UI_Int(1), "int1"),
      ],
      [
        (uilib.ui.value.UI_Int(2), "int2", 3),
      ],
      [
        (uilib.ui.value.UI_Int(3), "int3", 3, 1),
      ],
      [
        (uilib.ui.value.UI_Int(4), "", 3, 1, tkinter.E),
      ],
    ],
    as_single_value=True
  )
  built = ui_layout.build(test_toplevel)
  built.pack()
  assert ui_layout.get_value() == 1
  assert ui_layout.save_as_param() == [0, 1, 2, 3, 4]
  ui_layout.load_from_param([10, 11, 12, 13, 14])
  assert ui_layout.get_value() == 11
  assert ui_layout.save_as_param() == [10, 11, 12, 13, 14]
  with pytest.raises(ValueError):
    ui_layout.load_from_param(None)
