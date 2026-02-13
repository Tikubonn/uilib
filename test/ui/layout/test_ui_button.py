
import time
import uilib
import pytest
import tkinter

def test_ui_button (test_tk):
  ui_button = uilib.ui.layout.UI_Button("abc", lambda: None)
  built = ui_button.build(test_tk)
  built.pack()
  assert ui_button.get_value() is None
  assert ui_button.save_as_param() is None
  ui_button.load_from_param(123)
  assert ui_button.get_value() is None
  assert ui_button.save_as_param() is None
