
import uilib
import pytest
import tkinter

def test_ui_choices (test_tk):
  ui_choices = uilib.ui.value.UI_Choices(1, [1, 2, 3])
  built = ui_choices.build(test_tk)
  built.pack(fill=tkinter.X)
  assert ui_choices.get_value() == 1
  assert ui_choices.save_as_param() == "1"
  ui_choices.load_from_param("2")
  assert ui_choices.get_value() == 2
  assert ui_choices.save_as_param() == "2"
  with pytest.raises(ValueError):
    ui_choices.load_from_param(None)
