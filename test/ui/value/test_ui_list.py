
import time
import uilib
import pytest
import tkinter

def test_ui_list (test_tk):
  ui_list = uilib.ui.value.UI_List(
    [
      uilib.ui.value.UI_Int(0),
      uilib.ui.value.UI_Int(1),
      uilib.ui.value.UI_Int(2),
    ],
    add_func=lambda: uilib.ui.value.UI_Int(0)
  )
  built = ui_list.build(test_tk)
  built.pack(fill=tkinter.X)
  assert ui_list.get_value() == [0, 1, 2]
  assert ui_list.save_as_param() == [0, 1, 2]
  ui_list.load_from_param([3, 4, 5])
  assert ui_list.get_value() == [3, 4, 5]
  assert ui_list.save_as_param() == [3, 4, 5]
  with pytest.raises(ValueError):
    ui_list.load_from_param(None)
