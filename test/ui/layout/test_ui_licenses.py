
import uilib
import pytest
import tkinter

def test_ui_licenses (test_toplevel):
  ui_licenses = uilib.ui.layout.UI_Licenses([uilib.ui.layout.License("abc", "abc's license text.")])
  built = ui_licenses.build(test_toplevel)
  built.pack()
  assert ui_licenses.get_value() is None
  assert ui_licenses.save_as_param() is None
  ui_licenses.load_from_param(123)
  assert ui_licenses.get_value() is None
  assert ui_licenses.save_as_param() is None
