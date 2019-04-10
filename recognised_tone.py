
class Recognised_Tone:
    STone=None
    INumberOfRepeats=None

    def __init__(self, tone, repeats):
        self.STone=tone
        self.INumberOfRepeats=repeats

    def increaseNumberOfRepeats(self, val):
        self.INumberOfRepeats += val