
import uilib
import tkinter

tk = tkinter.Tk()
tooltip_label = tkinter.ttk.Label(tk, text="show the hint!")
tooltip_label.pack()
tooltip_text = " ".join(["this is hint!"] * 10)
uilib.ui.tkinter_.Tooltip(tooltip_label, text=tooltip_text)
other_label = tkinter.ttk.Label(tk, text="this is a plain text.")
other_label.pack()
tk.mainloop()
