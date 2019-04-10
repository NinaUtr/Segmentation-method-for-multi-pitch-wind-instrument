from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame
import soundfile
import winsound

class Music_Diagram(ttk.Frame):
    ASignals=None

    def __init__(self, parent, signals):
        super(Music_Diagram, self).__init__(parent)
        self.ASignals=signals

        figure1 = plt.Figure(figsize=(12, 10), dpi=50)
        #dt = 1 / self.ASignals[2]
        #time = numpy.linspace(0.0, len(self.ASignals[0]) * dt, len(self.ASignals[0]))
        Data1 = {'Amplitude': self.ASignals[0]}
        df1 = DataFrame(Data1)
        ax1 = figure1.add_subplot(111)
        diagram = FigureCanvasTkAgg(figure1, self)
        diagram.get_tk_widget().pack()
        df1.plot(ax=ax1)
        ax1.set_title("Rozpoznany dźwięk: "+self.ASignals[1],)

        playButton = ttk.Button(self, text="Graj", command=self.play)
        playButton.pack()

    def play(self):
        soundfile.write('new.wav', self.ASignals[0], self.ASignals[2])
        winsound.PlaySound('new.wav', winsound.SND_FILENAME)