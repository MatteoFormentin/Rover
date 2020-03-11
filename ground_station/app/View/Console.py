from tkinter import *


class Console(Toplevel):
    def __init__(self):
        super().__init__()
        self.configure(background="#282828")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.resizable(False, False)
        self.title("Console")

        # TEXT CONSOLE
        self.text = Text(self)
        self.text.config(background="#282828", font=("Monaco", 12), fg="white", height=20, width=40, borderwidth=1,
                         highlightthickness=1)
        self.text.config(state=DISABLED)
        self.text.grid(row=0, column=0)

        self.data = Text(self)
        self.data.config(background="#282828", font=("Monaco", 12), fg="white", height=20, width=40, borderwidth=1,
                         highlightthickness=1)
        self.data.config(state=DISABLED)
        self.data.grid(row=0, column=1)

    def on_close(self):
        pass

    def println(self, s=""):
        self.text.config(state=NORMAL)
        self.text.insert(END, " " + str(s) + '\n')
        self.text.see(END)
        self.text.config(state=DISABLED)

    def printData(self, s=""):
        self.data.config(state=NORMAL)
        self.data.insert(END, " " + str(s) + '\n')
        self.data.see(END)
        self.data.config(state=DISABLED)

    def clearData(self):
        self.data.config(state=NORMAL)
        self.data.delete(0.0, END)
        self.data.config(state=DISABLED)

    def clear(self):
        self.text.config(state=NORMAL)
        self.text.delete(0.0, END)
        self.text.config(state=DISABLED)
