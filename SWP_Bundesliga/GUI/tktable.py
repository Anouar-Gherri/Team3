class TkTabelle:

    def __init__(self, frame, zeilen, spalten):

        self.frame=frame

        self.zeilen=zeilen
        self.spalten=spalten
        self.tabelle=[]

        for z in range(zeilen):

            self.tabelle.append([])

            for s in range(spalten):
                entry=tk.Entry(frame)
                entry.grid(row=z, column=s)
                self.tabelle[-1].append(entry)

    def einfuegen(self, zeile, spalte, text):
        '''Fügt text ein'''

        self.tabelle[zeile - 1][spalte - 1].insert('end', text)