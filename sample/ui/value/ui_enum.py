
import uilib
import tkinter
import tkinter.ttk
from enum import Enum, auto, unique

@unique
class SampleEnum (Enum):

  A = auto()
  B = auto()
  C = auto()

def callback (value:SampleEnum):
  print("Changed to", value)

def pressed_on_print ():
  global ui
  global ui_readonly
  print(repr(ui.get_value()))
  print(repr(ui_readonly.get_value()))

tk = tkinter.Tk()
ui = uilib.ui.value.UI_Enum(
  SampleEnum.A, 
  SampleEnum, 
  label_table={
    SampleEnum.A: "Switch to A", 
    SampleEnum.B: "Switch to B", 
    SampleEnum.C: "Switch to C"
  }, 
  callback=callback
)
ui.build(tk).pack(padx=10, pady=(10, 0))
ui_readonly = uilib.ui.value.UI_Enum(
  SampleEnum.A, 
  SampleEnum, 
  label_table={
    SampleEnum.A: "Switch to A", 
    SampleEnum.B: "Switch to B", 
    SampleEnum.C: "Switch to C"
  }, 
  readonly=True,
  callback=callback
)
ui_readonly.build(tk).pack(padx=10, pady=(10, 0))
button = tkinter.ttk.Button(tk, text="Print", command=pressed_on_print)
button.pack(padx=10, pady=10)
tk.mainloop()
