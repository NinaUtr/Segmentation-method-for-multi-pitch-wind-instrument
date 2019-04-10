class Midi:
    SInstrument=None

    def __init__(self, instrument):
        self.SInstrument = instrument

    def range_of_midi(self):
        unique_midi = []
        if self.SInstrument=="flute":
            for i in range(60,97):
                unique_midi.append('0'+str(i))
        elif self.SInstrument=="oboe":
            for i in range(58,92):
                unique_midi.append('0'+str(i))
        elif self.SInstrument== "clarnet":
            for i in range(50,92):
                unique_midi.append('0'+str(i))
        return unique_midi