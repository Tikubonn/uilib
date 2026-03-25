
import uilib
import tkinter

tk = tkinter.Tk()
tooltip_label = tkinter.ttk.Label(tk, text="show the hint!")
tooltip_label.pack()
uilib.ui.tkinter_.Tooltip(tooltip_label, text="this is hint!")
other_label = tkinter.ttk.Label(tk, text="this is a plain text.")
other_label.pack()
tk.mainloop()
