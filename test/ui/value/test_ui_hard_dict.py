
import time
import uilib
import pytest
import tkinter

@pytest.fixture
def tk () -> tkinter.Tk:
  tk = tkinter.Tk()
  yield tk
  tk.destroy()
  time.sleep(1)

def test_ui_hard_dict (tk):
  ui_hard_dict = uilib.ui.value.UI_HardDict(
    {
      "a": uilib.ui.value.UI_Str("abc"),
      "b": uilib.ui.value.UI_Int(123)
    }, 
    label_table={
      "a": "A",
      "b": "B"
    }
  )
  built = ui_hard_dict.build(tk)
  built.pack(fill=tkinter.X)
  assert ui_hard_dict.get_value() == {"a": "abc", "b": 123}
  ui_hard_dict.load_from_param({"a": "def", "b": 456})
  assert ui_hard_dict.get_value() == {"a": "def", "b": 456}
  with pytest.raises(ValueError):
    ui_hard_dict.load_from_param(None)
  with pytest.raises(KeyError):
    ui_hard_dict.load_from_param({"c": "def"})
