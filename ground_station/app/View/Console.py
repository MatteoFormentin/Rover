from tkinter import *


class Console(Toplevel):
    def __init__(self, controller):
        super().__init__()
        self.configure(background="#282828")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.resizable(False, False)
        self.title("Console")

        self.controller = controller

        # TEXT CONSOLE
        self.text = Text(self)
        self.text.config(background="#282828", font=("Monaco", 12), fg="white", height=20, width=42, borderwidth=1,
                         highlightthickness=1)
        self.text.config(state=DISABLED)
        self.text.grid(row=0, column=0, columnspan=4)

        self.data = Text(self)
        self.data.config(background="#282828", font=("Monaco", 12), fg="white", height=20, width=42, borderwidth=1,
                         highlightthickness=1)
        self.data.config(state=DISABLED)
        self.data.grid(row=0, column=4)

        self.command_label = Label(self, text="Command:",
                                   background="#282828", fg="white")
        self.command_label.grid(row=1, column=0, sticky="E", pady=(20, 20))

        self.command_box = Entry(
            self, background="#282828", highlightbackground="#282828", fg="white", width=15)
        self.command_box.grid(row=1, column=1, sticky="W", pady=(20, 20))

        self.value_label = Label(self, text="Value:",
                                 background="#282828", fg="white")
        self.value_label.grid(row=1, column=2, sticky="E", pady=(20, 20))

        self.value_box = Entry(
            self, background="#282828", highlightbackground="#282828", fg="white", width=3)
        self.value_box.grid(row=1, column=3, sticky="E", pady=(20, 20))

        self.send_button = Button(
            self, text="SEND", background="#282828", highlightbackground="#282828", width=10, command=self.sendPressed)
        self.send_button.grid(row=1, column=4, sticky="W", pady=(20, 20))

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

    def sendPressed(self):
        self.controller.sendCommand(self.command_box.get(), self.value_box.get())
        self.command_box.delete(0, END)
        self.value_box.delete(0, END)
