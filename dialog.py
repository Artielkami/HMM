import Tkinter as Tk


class InfoDialog:

    def __init__(self, parent):

        top = self.top = Tk.Toplevel(parent)

        Tk.Label(top, text="Value").pack()

        self.e = Tk.Entry(top)
        self.e.pack(padx=5)

        b = Tk.Button(top, text="OK", command=self.ok)
        b.pack(pady=5)

    def ok(self):

        print "value is", self.e.get()

        self.top.destroy()