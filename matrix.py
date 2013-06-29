import Tkinter as tk
"""modified after http://stackoverflow.com/questions/11047803/creating-a-table-look-a-like-tkinter"""
class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        t = SimpleTable(self, 10,10)
        t.pack(side="top", fill="x")
        t.set(0,0,"Hello, world")

class SimpleTable(tk.Frame):
    def __init__(self, parent, rows=20, columns=20):
        # use black background so it "peeks through" to 
        # form grid lines
        tk.Frame.__init__(self, parent, background="black")
        self._widgets = []
        self.nRows=0
        self.nCols=0
        if rows>0 and columns >0:
            self.nRows=1
            self.nCols=1
            entry = MatrixEntry(self, value=0, borderwidth=0, width=10)
            entry.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
            print "Matirx: 0,0"
            self._widgets = [[entry]]

            self.addRows(rows-1)
            self.addCols(columns-1)

        self.initMenubar()

    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.set(value)

    def setColor(self, row, column, color):
        self._widgets[row][column].setColor(color)

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

    def fill(self, src):
        for i in src.psiDict:
            print i
            self.set(int(i[0]), int(i[1]), src.psiDict[i])
            if src.psiDict[i] < 0:
                self.setColor(int(i[0]), int(i[1]), "#ffaaaa")
            if src.psiDict[i] > 0:
                self.setColor(int(i[0]), int(i[1]), "#aaffaa")


    def addRows(self,n=1):
        for i in xrange(n):
            newRow = []
            for j in xrange(self.nCols):
                entry = MatrixEntry(self, value=0, 
                                    borderwidth=0, width=10)
                entry.grid(row=self.nRows+i, column=j, sticky="nsew", 
                           padx=1, pady=1)
                print "Matrix: %s/%s - %s/%s"%(self.nRows+i, j, self.nRows,self.nCols)
                newRow.append(entry)
                self._widgets.append(newRow)
        self.nRows +=n


    def addCols(self,n=1):
        for i in xrange(self.nRows):
            for j in xrange(n):
                entry = MatrixEntry(self, value=0, 
                                    borderwidth=0, width=10)
                entry.grid(row=i, column=self.nCols+j, sticky="nsew", 
                           padx=1, pady=1)
                print "Matrix: %s/%s - %s/%s"%(i, self.nCols+j, self.nRows,self.nCols)
                self._widgets[i].append(entry)
        self.nCols +=n


if __name__ == "__main__":
    app = ExampleApp()
    app.mainloop()


class MatrixEntry(tk.Frame):
    """
        a class for a single entry in the data matrix. It should contain an edit with an attached doubleVar
    """
    def __init__(self,master,value=0,**kwargs):
        self.value = value 
        tk.Frame.__init__(self, master, background="white",**kwargs)
        self.text = tk.StringVar()
        self.edit = tk.Entry(self, width=6, textvariable = self.text)
        self.edit.insert(0, "%2.4f"%self.value )
        self.text.trace("w", lambda a,b,c,n=self.edit : self.updateValue(a,n))
        self.edit.pack()

    def updateValue(self,ele , field):
        val = field.get()
        b , v = self.toFloat(val)
        if b:
            self.value = v
        else:
            self.edit.delete(0,tk.END)
            self.edit.insert(0, "%2.4f"%self.value )


    @staticmethod
    def toFloat(val):
        if val == "":
            return True,0
        try:
            v = float(val)
        except ValueError:
            return False,None
        return True, v

    def get(self):
        return self.value

    def set(self, x):
        self.value = x
        self.text = "%2.4f"%self.value 
        self.edit.delete(0,tk.END)
        self.edit.insert(0, self.text)
        print "set", x

    def setColor(self, x):
        self.edit.configure(bg=x)

