from numpy import concatenate
from sklearn import mixture


class GMM_Model:
    SMidi=None
    SCovariances='spherical'
    IComponent=39
    DMfccs=None


    def __init__(self, midi, mfccs):
        self.Midi=midi
        self.DMfccs=mfccs

    def model(self):
        gmms=[]
        for midi in self.Midi:
            first_value= False
            for key, element in self.DMfccs.items():
                if key == midi:
                    if first_value == False:
                        mfcc = self.DMfccs[key]
                        first_value = True
                    else :
                        mfcc = concatenate((mfcc, self.DMfccs[key]), axis=0)

            gmix = mixture.GaussianMixture(self.IComponent, self.SCovariances)
            gmms.append(gmix.fit(mfcc))
        return gmms