
import uilib
import pytest
import tkinter

def test_ui_text (test_toplevel):
  ui_text = uilib.ui.layout.UI_Text("abc")
  built = ui_text.build(test_toplevel)
  built.pack()
  assert ui_text.get_value() is None
  assert ui_text.save_as_param() is None
  ui_text.load_from_param(123)
  assert ui_text.get_value() is None
  assert ui_text.save_as_param() is None
