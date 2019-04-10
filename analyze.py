from gmm_model import GMM_Model
from recognition import Recognition
from end_results import End_Results
from mfcc_generator import Mfcc_Generator
from midi import Midi
import threading

class Analyze(threading.Thread):
    SInstrument=None
    SPathUnknown=None

    def __init__(self,instrument,path_unknown,callback,callback_progress):
        super(Analyze,self).__init__()
        self.SInstrument=instrument
        self.SPathUnknown=path_unknown
        self.Callback = callback
        self.CallbackProgress = callback_progress

    def run(self):
        #tworzymy lub pobieramy wartości mfcc
        [MG_train, MG_unknown, M_midi]=self.instrument_variant()
        mfcc_library=MG_train.import_or_make_mfcc()
        mfcc_unknown=MG_unknown.import_or_make_mfcc()

        #sprawdzamy jaki jest zakres dźwięków midi
        midi=M_midi.range_of_midi()

        #tworzymy modele dźwieków midi
        gmms=GMM_Model(midi,mfcc_library).model()

        #rozpoznajemy wysokosci we wszystkich plikach z podanego folderu
        recognition=Recognition(gmms,mfcc_unknown,midi).rec_every_unknown()

        #ostatecznie przyporządkowujemy wysokości
        end_result=End_Results(recognition,self.SInstrument,self.SPathUnknown,self.CallbackProgress).end_result_for_each()
        if self.Callback is not None:
            self.Callback(end_result)

    def instrument_variant(self):
        path_library = ["library/" + self.SInstrument, True, self.SInstrument]
        path_unknown = [self.SPathUnknown, False, self.SInstrument]

        MG_train = Mfcc_Generator(
            path_library[0],
            train=path_library[1],
            instrument=path_library[2])

        MG_unknown = Mfcc_Generator(
            path_unknown[0],
            train=path_unknown[1],
            instrument=path_unknown[2])

        M_midi = Midi(self.SInstrument)
        return MG_train, MG_unknown, M_midi