
import time
import uilib
import pytest
import tkinter

def test_ui_path (test_tk):
  ui_path = uilib.ui.value.UI_Path("abc", uilib.ui.value.PathType.FILE)
  built = ui_path.build(test_tk)
  built.pack(fill=tkinter.X)
  assert ui_path.get_value() == "abc"
  assert ui_path.save_as_param() == "abc"
  ui_path.load_from_param("def")
  assert ui_path.get_value() == "def"
  assert ui_path.save_as_param() == "def"
  with pytest.raises(ValueError):
    ui_path.load_from_param(None)
