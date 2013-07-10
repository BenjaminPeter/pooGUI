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
            entry.grid(row=1, column=1, sticky="nsew", padx=1, pady=1)
            print "Matirx: 0,0"
            self._widgets = [[entry]]
            self._topleftCell = MatrixLabel(self)
            self._topleftCell.grid(row=0, column=0, sticky="nsew")
            self._rowLabels = [MatrixLabel(self)]
            self._colLabels = [MatrixLabel(self)]
            self._colLabels[0].grid(row=0, column=1, sticky="nsew")
            self._rowLabels[0].grid(row=1, column=0, sticky="nsew")

            self.addRows(rows-1)
            self.addCols(columns-1)


            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)

        #self.initMenubar()

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
        self.menubar.add_cascade(label="Statistic top/right", menu=menu)
        menu.add_command(label="Directionality Index")
        menu.add_command(label="Z - Score (Binomial test)")
        menu.add_command(label="Z - Score (Block Jackknife)")
        menu.add_command(label="Diff in Heterozygosity")
        menu.add_command(label="FST")

        self.menubar.add_cascade(label="Statistic bottom/left", menu=menu)
        menu.add_command(label="Directionality Index")
        menu.add_command(label="Z - Score (Binomial test)")
        menu.add_command(label="Z - Score (Block Jackknife)")
        menu.add_command(label="Diff in Heterozygosity")
        menu.add_command(label="FST")

        self.menubar.add_cascade(label="Sort", menu=menu)
        menu.add_command(label="Default")
        menu.add_command(label="Cluster")
        menu.add_command(label="Statistic")


        self.master.config(menu=self.menubar)
        print "SimpleTable.initMenubar: end"

    def fill_labels(self, sList):
        """
            Fills the Matrix labels.
            @param pop_order: the order where populations are
            @type pop_order: dict[Population] => order
        """
        for i,sample in enumerate(sList):
            self._colLabels[i].set(sample.name)
            self._rowLabels[i].set(sample.name)
            self._colLabels[i].set_color(sample.cstr)
            self._rowLabels[i].set_color(sample.cstr)

    def fill(self, sList, stat):
        """
            Fills the upper Matrix triangle with a pairwise statistc.
            @param pop_order: the order where populations are
            @type pop_order: dict[Population] => order
            @param stat: the statistic to be filled in
            @type stat: dict[Population,Population] => statistic
        """
        self.stat_upper = stat
        for i,s1 in enumerate(sList):
            for j0,s2 in enumerate(sList[i+1:]):
                j = j0 + i + 1
                self.set(i,j, stat[s1.pop, s2.pop])

                #some basic coloring
                if stat[s1.pop,s2.pop] < 0:
                    self.setColor(i,j, "#ffaaaa")
                if stat[s1.pop,s2.pop] > 0:
                    self.setColor(i,j, "#aaffaa")


    def addRows(self,n=1):
        for i in xrange(n):
            newRow = []
            for j in xrange(self.nCols):
                entry = MatrixEntry(self, value=0, 
                                    borderwidth=0, width=10)
                entry.grid(row=self.nRows+i+1, column=j+1,
                           sticky="nsew", 
                           padx=1, pady=1)
                newRow.append(entry)
                self._widgets.append(newRow)
            lab = MatrixLabel(self,"blaa")
            lab.grid(row=self.nRows+i+1, column=0, sticky="nsew")
            self._rowLabels.append(lab)
        self.nRows +=n


    def addCols(self,n=1):
        for i in xrange(self.nRows):
            for j in xrange(n):
                entry = MatrixEntry(self, value=0, 
                                    borderwidth=0, width=10)
                entry.grid(row=i+1, column=self.nCols+j+1,
                           sticky="nsew", 
                           padx=1, pady=1)
                self._widgets[i].append(entry)
        for j in xrange(n):
            lab = MatrixLabel(self,"Blluuu%d"%i)
            self._colLabels.append(lab)
            lab.grid(column=self.nCols+j+1, row=0, sticky="nsew")
        self.nCols +=n

    def update_sample_order(self, sList):
        """
            updates the order the sample appear in the Matrix
        """
        self.fill_labels(sList)
        self.fill(sList, self.stat_upper)

class MatrixLabel(tk.Frame):
    """
        the labels of the statistics matrix
    """
    def __init__(self,master, value="", **kwargs):
        tk.Frame.__init__(self, master, background="blue",
                           **kwargs)
        self.text = tk.StringVar()
        self.label = tk.Label(self, textvariable = self.text, bg="pink", anchor = tk.CENTER, font="bold")
        self.text.set(value)
        self.label.grid(sticky="nsew")
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)

    def set(self, x):
        self.text.set(x)

    def set_color(self,c):
        self.label.config(bg=c)

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
        self.text.set("%2.4f"%self.value)

    def setColor(self, x):
        self.edit.configure(bg=x)

if __name__ == "__main__":
    app = ExampleApp()
    app.mainloop()
