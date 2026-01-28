
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

def test_ui_dict (tk):
  ui_dict = uilib.ui.value.UI_Dict(
    {
      "a": uilib.ui.value.UI_Int(0),
      "b": uilib.ui.value.UI_Int(1),
      "c": uilib.ui.value.UI_Int(2),
    },
    add_func=lambda: uilib.ui.value.UI_Int(0)
  )
  built = ui_dict.build(tk)
  built.pack(fill=tkinter.X)
  assert ui_dict.get_value() == {"a": 0, "b": 1, "c": 2}
  ui_dict.load_from_param({"d": 3, "e": 4, "f": 5})
  assert ui_dict.get_value() == {"d": 3, "e": 4, "f": 5}
  with pytest.raises(ValueError):
    ui_dict.load_from_param(None)
