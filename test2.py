import Tkinter as tk

class MatrixLabel(tk.Frame):
    """
        the labels of the statistics matrix
    """
    def __init__(self,master, value="", **kwargs):
        tk.Frame.__init__(self, master, background="blue",
                          **kwargs)
        self.text = tk.StringVar()
        self.label = tk.Label(self, textvariable = self.text, bg="pink", anchor = tk.CENTER)
        self.text.set(value)
        self.label.grid(sticky="nsew")
    def set(self, x):
        self.text.set(x)


root = tk.Tk()
ml = MatrixLabel(root)
ml.set("bla")
ml.grid(sticky="nsew")
ml.columnconfigure(0,weight=1)
ml.rowconfigure(0,weight=1)
root.columnconfigure(0,weight=1)
root.rowconfigure(0,weight=1)


root.mainloop()

