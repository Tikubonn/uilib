
import uilib
import pytest
import tkinter

def test_ui_str (test_toplevel):
  ui_str = uilib.ui.value.UI_Str("abc")
  built = ui_str.build(test_toplevel)
  built.pack(fill=tkinter.X)
  assert ui_str.get_value() == "abc"
  assert ui_str.save_as_param() == "abc"
  ui_str.load_from_param("def")
  assert ui_str.get_value() == "def"
  assert ui_str.save_as_param() == "def"
  with pytest.raises(ValueError):
    ui_str.load_from_param(None)

def test_ui_str_readonly (test_toplevel):
  ui_str = uilib.ui.value.UI_Str("abc", readonly=True)
  built = ui_str.build(test_toplevel)
  built.pack(fill=tkinter.X)
  assert ui_str.get_value() == "abc"
  assert ui_str.save_as_param() == "abc"
  ui_str.load_from_param("def")
  assert ui_str.get_value() == "abc"
  assert ui_str.save_as_param() == "abc"
