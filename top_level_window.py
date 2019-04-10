from tkinter import *
from music_diagram import Music_Diagram


class Top_Level_Window(Toplevel):
    ASignals=None

    def __init__(self, song_name, signals):
        super(Top_Level_Window, self).__init__()
        self.ASignals = signals
        self.title(song_name)
        self.configure(bg="#424242")

        canvas = Canvas(self, width=1200, height=600,
                           background="#424242",
                           scrollregion=(0, 0, 3000, 600))

        canvas.scrollX = Scrollbar(self, orient=HORIZONTAL)
        canvas['xscrollcommand'] = canvas.scrollX.set
        canvas.scrollX['command'] = canvas.xview

        emptyFrame=Frame(canvas)
        emptyFrame.winfo_width()
        iteration=0
        for tone in self.ASignals:
            frame = Music_Diagram(emptyFrame, tone)
            frame.grid(row=0, column=iteration)
            iteration += 1

        canvas.create_window((0, 0), window=emptyFrame, anchor='nw')
        canvas.scrollX.pack(side=BOTTOM, fill=X)
        canvas.pack(side=LEFT)


