import Tkinter as tk
"""modified after http://stackoverflow.com/questions/11047803/creating-a-table-look-a-like-tkinter"""
class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        t = SimpleTable(self, 10,10)
        t.pack(side="top", fill="x")
        t.set(0,0,"Hello, world")

class SimpleTable(tk.Frame):
    def __init__(self, parent, rows=10, columns=2):
        # use black background so it "peeks through" to 
        # form grid lines
        tk.Frame.__init__(self, parent, background="black")
        self._widgets = []
        for row in range(rows):
            current_row = []
            for column in range(columns):
                label = tk.Label(self, text="%s/%s" % (row, column), 
                                 borderwidth=0, width=10)
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(label)
            self._widgets.append(current_row)

        self.initMenubar()

    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=str(value))

    def setColor(self, row, column, color):
        pass

    def initMenubar(self):
        """
        this function loads and populates the menubar, and will register its events
        """
        self.menubar = tk.Menu(self)

        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Statistic", menu=menu)
        menu.add_command(label="Directionality Index")
        menu.add_command(label="Z - Score (Binomial test)")
        menu.add_command(label="Z - Score (Block Jackknife)")
        menu.add_command(label="Diff in Heterozygosity")
        menu.add_command(label="FST")

        self.menubar.add_cascade(label="Order", menu=menu)
        menu.add_command(label="Default")
        menu.add_command(label="Statistic")


        self.master.config(menu=self.menubar)
        print "SimpleTable.initMenubar: end"

if __name__ == "__main__":
    app = ExampleApp()
    app.mainloop()
