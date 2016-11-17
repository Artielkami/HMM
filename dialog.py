import Tkinter as tk
import tkMessageBox as tkmsg
import logging
loger = logging.getLogger('Dialog')


def show_error(self, error_tittle, message):
    tkmsg.showerror(title=error_tittle, message=message)
    return False


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

    def __init__(self, parent, var):

        top = self.top = tk.Toplevel(parent)
        top.lift()
        top.attributes('-topmost', True)
        tk.Label(top, text="Value").pack()

        self.e = tk.Entry(top)
        self.e.pack(padx=5)

        self.var = var

        b = tk.Button(top, text="OK", command=self.ok)
        b.pack(pady=5)

    def ok(self):
        try:
            k = int(self.e.get())
            self.var.set(k)
            loger.info("value is %d" % k)
            self.top.destroy()
            return True
        except ValueError:
            tkmsg.showerror(title='Input Error', message='Invalid input for day search number, '
                                                         'please insert a integer number')
            return False
