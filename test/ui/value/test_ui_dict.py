
import time
import uilib
import pytest
import tkinter

def test_ui_dict (test_tk):
  ui_dict = uilib.ui.value.UI_Dict(
    {
      "a": uilib.ui.value.UI_Int(0),
      "b": uilib.ui.value.UI_Int(1),
      "c": uilib.ui.value.UI_Int(2),
    },
    add_func=lambda: uilib.ui.value.UI_Int(0)
  )
  built = ui_dict.build(test_tk)
  built.pack(fill=tkinter.X)
  assert ui_dict.get_value() == {"a": 0, "b": 1, "c": 2}
  assert ui_dict.save_as_param() == {"a": 0, "b": 1, "c": 2}
  ui_dict.load_from_param({"d": 3, "e": 4, "f": 5})
  assert ui_dict.get_value() == {"d": 3, "e": 4, "f": 5}
  assert ui_dict.save_as_param() == {"d": 3, "e": 4, "f": 5}
  with pytest.raises(ValueError):
    ui_dict.load_from_param(None)
