
import uilib
import tkinter
from enum import Enum, auto, unique

@unique
class SampleEnum (Enum):

  A = auto()
  B = auto()
  C = auto()

tk = tkinter.Tk()
tk.title("Sample window")
tk.minsize(320, 240)
ui = uilib.ui.value.UI_Enum(SampleEnum.A, SampleEnum, {SampleEnum.A: "Switch to A", SampleEnum.B: "Switch to B", SampleEnum.C: "Switch to C"})
ui.build(tk).pack(padx=10, pady=10)
button = tkinter.Button(tk, text="Print", command=lambda: print(repr(ui.get_value())))
button.pack(padx=10, pady=(0, 10))
tk.mainloop()
