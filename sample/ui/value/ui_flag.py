
import uilib
import tkinter
from enum import Flag, auto, unique

@unique
class SampleFlag (Flag):

  A = auto()
  B = auto()
  C = auto()

def callback (value:SampleFlag):
  print("Changed to", value)

tk = tkinter.Tk()
tk.title("Sample window")
tk.minsize(320, 240)
ui = uilib.ui.value.UI_Flag(
  SampleFlag.A|SampleFlag.B|SampleFlag.C, 
  SampleFlag, 
  {
    SampleFlag.A: "Toggle A", 
    SampleFlag.B: "Toggle B", 
    SampleFlag.C: "Toggle C"
  },
  callback=callback
)
ui.build(tk).pack(padx=10, pady=10)
button = tkinter.Button(tk, text="Print", command=lambda: print(repr(ui.get_value())))
button.pack(padx=10, pady=(0, 10))
tk.mainloop()
