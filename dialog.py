import Tkinter as tk


class StatusBar(tk.Frame):
    """ Status bar for application """
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.variable = tk.StringVar()
        self.label = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W,
                              textvariable=self.variable,
                              font=('arial', 16, 'normal'),
                              padx=10)
        self.variable.set('Status Bar')
        self.label.pack(fill=tk.X)
        self.grid(columnspan=2, sticky='we')

    def set_status(self, text, *args, **kwargs):
        self.variable.set(text)

    def clear_status(self):
        self.variable.set('')


class InfoDialog:

    def __init__(self, parent):

        top = self.top = tk.Toplevel(parent)

        tk.Label(top, text="Value").pack()

        self.e = tk.Entry(top)
        self.e.pack(padx=5)

        b = tk.Button(top, text="OK", command=self.ok)
        b.pack(pady=5)

    def ok(self):

        print "value is", self.e.get()

        self.top.destroy()