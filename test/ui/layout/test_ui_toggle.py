
import uilib
import pytest
import tkinter

def test_ui_toggle (test_toplevel):
  ui_toggle = uilib.ui.layout.UI_Toggle(
    uilib.ui.value.UI_Int(123)
  )
  built = ui_toggle.build(test_toplevel)
  built.pack()
  assert ui_toggle.get_value() == 123
  assert ui_toggle.save_as_param() == 123
  ui_toggle.load_from_param(456)
  assert ui_toggle.get_value() == 456
  assert ui_toggle.save_as_param() == 456
