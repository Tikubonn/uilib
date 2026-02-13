
import pytest
import tkinter

@pytest.fixture
def test_tk () -> tkinter.Tk:
  tk = tkinter.Tk()
  yield tk
  tk.destroy()
  # tk.quit()
