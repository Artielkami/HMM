import Tkinter as tk
import tkMessageBox as tkmsg
from tkFileDialog import askopenfilename


class TpFrame(object):
    def __init__(self, master=None, **kwargs):
        self.frame = tk.Frame(master=master, **kwargs)
        self.frame.pack(fill=tk.X, padx=10, pady=10)
        f = tk.Frame(self.frame, **kwargs)
        f.pack(fill=tk.X)
        w = tk.Label(f, text="Table transits probability", fg="blue", anchor=tk.W, justify=tk.LEFT)
        w.pack(fill=tk.X, padx=10, pady=10, side=tk.LEFT)
        # w.grid(row=0, column=0,)
        # make table transit probability
        g = tk.Frame(self.frame, **kwargs)
        g.pack(fill=tk.X, side=tk.LEFT)
        # f.grid(row=1, column=0)
        for i in range(1, 4, 1):
            for j in range(0, 3, 1):
                w = tk.Entry(g)
                w.grid(row=i, column=j)


class TeFrame(object):
    def __init__(self, master=None, **kwargs):
        # frame table + label
        self.frame = tk.Frame(master=master, **kwargs)
        self.frame.pack(fill=tk.X, padx=10, pady=10)
        # frame for label
        f = tk.Frame(self.frame, **kwargs)
        f.pack(fill=tk.X)
        w = tk.Label(f, text="Table emission probability", fg="blue", anchor=tk.W, justify=tk.LEFT)
        w.pack(fill=tk.X, padx=10, pady=10, side=tk.LEFT)
        # frame for table
        g = tk.Frame(self.frame, **kwargs)
        g.pack(fill=tk.X)
        # make table transit probability
        for i in range(1, 4, 1):
            for j in range(0, 2, 1):
                w = tk.Entry(g)
                w.grid(row=i, column=j)


class ImportButton(object):
    def __init__(self, master=None, **kwargs):
        # frame table + label
        self.frame = tk.Frame(master=master, **kwargs)
        self.frame.pack(fill=tk.X, padx=10, pady=10, side=tk.LEFT)
        w = tk.Label(self.frame, text="Table emission probability", fg="blue", justify=tk.LEFT)
        w.pack(fill=tk.X, padx=10, pady=10, side=tk.LEFT)


class Dialog(tk.Tk):

    def __init__(self, setting=None, *args, **kwargs):

        self.master = tk.Tk.__init__(self, *args, **kwargs)
        # tk.Button(text='Quit', command=self.callback).pack(fill=tk.X)
        # tk.Button(text='Answer', command=self.answer).pack(fill=tk.X)
        self.title(setting['title'])
        self.geometry(setting['geometry'])
        self.left_frame = tk.Frame(master=self.master, **kwargs)
        self.left_frame.grid(row=0, column=0)
        self.right_frame = tk.Frame(master=self.master, **kwargs)
        self.right_frame.grid(row=0, column=1, sticky=tk.NW)
        TpFrame(self.left_frame)
        TeFrame(self.left_frame)
        ImportButton(self.right_frame)

        menu = tk.Menu(self)
        self.config(menu=menu)
        filemenu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New", command=self.NewFile)
        filemenu.add_command(label="Open...", command=self.OpenFile)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)

        helpmenu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.About)

    def NewFile(self):
        print "New File!"

    def OpenFile(self):
        name = askopenfilename()
        print name

    def About(self):
        print "This is a simple example of a menu"

    def answer(self):
        tkmsg.showerror("Answer", "Sorry, no answer available")

    def callback(sel):
        if tkmsg.askyesno('Verify', 'Really quit?'):
            tkmsg.showwarning('Yes', 'Not yet implemented')
        else:
            tkmsg.showinfo('No', 'Quit has been cancelled')

