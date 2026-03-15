
import uilib
import pytest
import tkinter

def test_ui_tab (test_toplevel):
  ui_tab = uilib.ui.layout.UI_Tab(
    {
      "a": uilib.ui.value.UI_Int(1, (1, 100, 1)),
      "b": uilib.ui.value.UI_Int(2, (1, 100, 1)),
      "c": uilib.ui.value.UI_Int(3, (1, 100, 1)),
    }
  )
  built = ui_tab.build(test_toplevel)
  built.pack()
  assert ui_tab.get_value() == {"a": 1, "b": 2, "c": 3}
  assert ui_tab.save_as_param() == {"a": 1, "b": 2, "c": 3}
  ui_tab.load_from_param({"a": 10, "b": 20, "c": 30})
  assert ui_tab.get_value() == {"a": 10, "b": 20, "c": 30}
  assert ui_tab.save_as_param() == {"a": 10, "b": 20, "c": 30}
  with pytest.raises(KeyError):
    ui_tab.load_from_param({"a": 10, "b": 20, "c": 30, "d": 40}) #存在しない要素ならば例外を送出する
  with pytest.raises(ValueError):
    ui_tab.load_from_param(None)
