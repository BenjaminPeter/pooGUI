import Tkinter as tk

class StatusBar(tk.Frame):
    """very simple statusbar for various progress messages and stuff"""
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.status = tk.StringVar()
        self.statusLabel = tk.Label(self, anchor=tk.W, textvariable = self.status)
        self.statusLabel.grid(sticky="nsew")
        self.status.set("STATUSMOFO")
        print "STATUS"

    def set(self,x):
        self.status.set(x)
    def clear(self):
        self.status.set(" ")

