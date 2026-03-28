
import uilib
import pytest
import tkinter

def test_ui_hint (test_toplevel):
  ui_hint = uilib.ui.layout.UI_Hint("abc")
  built = ui_hint.build(test_toplevel)
  built.pack()
  assert ui_hint.get_value() is None
  assert ui_hint.save_as_param() is None
  ui_hint.load_from_param(None)
  assert ui_hint.get_value() is None
  assert ui_hint.save_as_param() is None
  with pytest.raises(ValueError):
    ui_hint.load_from_param(123)
