
import pytest
import tkinter

@pytest.fixture(scope="session")
def test_tk () -> tkinter.Tk:
  tk = tkinter.Tk()
  yield tk
  tk.destroy()

@pytest.fixture
def test_toplevel (test_tk) -> tkinter.Toplevel:
  toplevel = tkinter.Toplevel(test_tk)
  yield toplevel
  toplevel.destroy()
