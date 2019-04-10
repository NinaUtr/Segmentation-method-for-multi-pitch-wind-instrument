from python_speech_features import mfcc
from python_speech_features import delta
import numpy
import os
import pickle
from soundfile import read


class Mfcc_Generator:
    SPath=None
    SInstrument=None
    FWindow_Len=0.02
    FWindow_Step =0.015
    INumcep=20
    INfiltr = 20
    ILowfreq=200
    IHighfreq = 3000
    BAppendEnergy = False
    BTrain=None

    def __init__(self, path, train, instrument):
        self.SPath = path
        self.BTrain = train
        self.SInstrument = instrument


    def import_or_make_mfcc(self):
        path="mfcc/"+self.name_of_the_mfcc_file()
        if not (os.path.isfile(path)):
            return self.make_mfcc()
        else:
            return self.import_mfcc()

    def name_of_the_mfcc_file(self):

        if self.BTrain == True:
            name_of_the_file = "mfccs_" + self.SInstrument + ".p"
        elif self.BTrain == False:
            name_of_the_file = "mfccs_unknown_" + self.SInstrument + ".p"

        return name_of_the_file

    def make_mfcc(self):
        out = {}
        for filename in os.listdir(self.SPath):

            if filename.endswith(".wav"):
                sig, fs = read(os.path.join(self.SPath, filename))
                norm_sig = sig / max(sig)

                if self.BTrain == True:
                    key = filename[11:14]
                elif self.BTrain== False:
                    key = filename

                mfcc_unknown= mfcc(
                        norm_sig,
                        fs,
                        winlen=self.FWindow_Len,
                        winstep=self.FWindow_Step,
                        numcep=self.INumcep,
                        nfilt=self.INfiltr,
                        nfft=int(self.FWindow_Len * fs),
                        highfreq=self.IHighfreq,
                        lowfreq=self.ILowfreq,
                        appendEnergy=self.BAppendEnergy
                    )
                delta_from_mfcc = delta(mfcc_unknown, N=2)
                delta_delta = delta(delta_from_mfcc, N=2)
                mfcc_unknown = numpy.concatenate((mfcc_unknown, delta_from_mfcc), axis=1)
                mfcc_unknown = numpy.concatenate((mfcc_unknown, delta_delta), axis=1)
                out[key]=mfcc_unknown

        pickle.dump(out, open("mfcc/"+self.name_of_the_mfcc_file(), "wb"))

        return self.import_mfcc()

    def import_mfcc(self):

        mfccs = pickle.load(open("mfcc/"+self.name_of_the_mfcc_file(), "rb"))

        return mfccs