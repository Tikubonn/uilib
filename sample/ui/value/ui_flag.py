
import uilib
import tkinter
import tkinter.ttk
from enum import Flag, auto, unique

@unique
class SampleFlag (Flag):

  A = auto()
  B = auto()
  C = auto()

def callback (value:SampleFlag):
  print("Changed to", value)

def pressed_on_print ():
  global ui
  global ui_readonly
  print(repr(ui.get_value()))
  print(repr(ui_readonly.get_value()))

tk = tkinter.Tk()
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
ui.build(tk).pack(padx=10, pady=(10, 0))
ui_readonly = uilib.ui.value.UI_Flag(
  SampleFlag.A|SampleFlag.B|SampleFlag.C, 
  SampleFlag, 
  {
    SampleFlag.A: "Toggle A", 
    SampleFlag.B: "Toggle B", 
    SampleFlag.C: "Toggle C"
  },
  readonly=True,
  callback=callback
)
ui_readonly.build(tk).pack(padx=10, pady=(10, 0))
button = tkinter.ttk.Button(tk, text="Print", command=pressed_on_print)
button.pack(padx=10, pady=10)
tk.mainloop()
