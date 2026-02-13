
import uilib
import tkinter

tk = tkinter.Tk()
scrollable = uilib.ui.tkinter_.Scrollable(tk, lambda master: tkinter.Listbox(master, height=5))
scrollable.pack(fill=tkinter.X)
for i in range(10):
  scrollable.widget.insert(tkinter.END, "item{:d}".format(i + 1))
tk.mainloop()
