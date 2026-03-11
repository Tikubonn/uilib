
import uilib
import pytest
import tkinter

def test_ui_inet_address (test_toplevel):
  ui_str = uilib.ui.value.UI_InetAddress(("127.0.0.1", 8080))
  built = ui_str.build(test_toplevel)
  built.pack(fill=tkinter.X)
  assert ui_str.get_value() == ("127.0.0.1", 8080)
  assert ui_str.save_as_param() == {
    "host": "127.0.0.1",
    "port": 8080
  }
  ui_str.load_from_param({
    "host": "example.com",
    "port": 80
  })
  assert ui_str.get_value() == ("example.com", 80)
  assert ui_str.save_as_param() == {
    "host": "example.com",
    "port": 80
  }
  with pytest.raises(ValueError):
    ui_str.load_from_param(None)

def test_ui_inet_address_readonly (test_toplevel):
  ui_str = uilib.ui.value.UI_InetAddress(("127.0.0.1", 8080), readonly=True)
  built = ui_str.build(test_toplevel)
  built.pack(fill=tkinter.X)
  assert ui_str.get_value() == ("127.0.0.1", 8080)
  assert ui_str.save_as_param() == {
    "host": "127.0.0.1",
    "port": 8080
  }
  ui_str.load_from_param({
    "host": "example.com",
    "port": 80
  })
  assert ui_str.get_value() == ("127.0.0.1", 8080)
  assert ui_str.save_as_param() == {
    "host": "127.0.0.1",
    "port": 8080
  }
