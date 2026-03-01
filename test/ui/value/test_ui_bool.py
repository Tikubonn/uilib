
import uilib
import pytest
import tkinter

def test_ui_bool (test_toplevel):
  ui_bool = uilib.ui.value.UI_Bool(False)
  built = ui_bool.build(test_toplevel)
  built.pack(fill=tkinter.X)
  assert ui_bool.get_value() == False
  assert ui_bool.save_as_param() == False
  ui_bool.load_from_param(True)
  assert ui_bool.get_value() == True
  assert ui_bool.save_as_param() == True
  with pytest.raises(ValueError):
    ui_bool.load_from_param(None)
