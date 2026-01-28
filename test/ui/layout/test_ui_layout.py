
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

def test_ui_layout (tk):
  ints = [uilib.ui.value.UI_Int(i) for i in range(10)]
  ui_layout = uilib.ui.layout.UI_Layout(
    [
      [
        ints[0],
        (ints[1], 2),
      ],
      [
        (ints[2], 2, 2),
      ],
      [
        (ints[3], 2, 2, uilib.enum_.Direction.E),
      ],
    ],
    {
      "int0": ints[0], 
      "int1": ints[1], 
      "int2": ints[2], 
      "int3": ints[3]
    }
  )
  built = ui_layout.build(tk)
  built.pack()
  assert ui_layout.get_value() == {"int0": 0, "int1": 1, "int2": 2, "int3": 3}
  ui_layout.load_from_param({"int0": 4, "int1": 5, "int2": 6, "int3": 7})
  assert ui_layout.get_value() == {"int0": 4, "int1": 5, "int2": 6, "int3": 7}
  with pytest.raises(ValueError):
    ui_layout.load_from_param(None)
  with pytest.raises(KeyError):
    ui_layout.load_from_param({"int0": 4, "int1": 5, "int2": 6, "int3": 7, "intX": -1})

def test_ui_layout_single_value (tk):
  ui_int = uilib.ui.value.UI_Int(123)
  ui_layout = uilib.ui.layout.UI_Layout(
    [[ui_int]],
    ui_int
  )
  built = ui_layout.build(tk)
  built.pack()
  assert ui_layout.get_value() == 123
  ui_layout.load_from_param(456)
  assert ui_layout.get_value() == 456
