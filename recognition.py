import numpy
from math import floor


class Recognition:
    DGmm_Model=None
    DMfcc_Unknown=None
    SMidi=None

    def __init__(self, gmm_model,mfcc_unknown,midi):
        self.DGmm_Model = gmm_model
        self.DMfcc_Unknown=mfcc_unknown
        self.SMidi=midi

    def rec_every_unknown(self):
        out=[]
        for key,element in self.DMfcc_Unknown.items():
            out.append(self.likelihoods(element, key))
        return out

    def likelihoods(self,mfcc_unknown,key):
        out=[]
        out2={}
        samples=2
        iterations = floor(len(mfcc_unknown) / samples)
        for i in range(iterations):
            propability = [numpy.mean(GMM.score(mfcc_unknown[i*samples:(i+1)*samples])) for GMM in self.DGmm_Model]
            max_prop_index=numpy.argmax(propability)
            out.append(self.SMidi[max_prop_index])
        out2[key]=out
        return out2