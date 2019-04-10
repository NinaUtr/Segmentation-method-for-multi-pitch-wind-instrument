from matplotlib import pyplot as plt
from sklearn import mixture
import numpy as np
import os
from soundfile import read
from python_speech_features import mfcc
from python_speech_features import delta
from numpy import concatenate

def make_mfcc():
    out = {}
    for filename in os.listdir("C:/Users/NinaNina/Desktop/Studia!/Inzynierka/proba_mfcc/test"):
        if filename.endswith(".wav"):
            sig, fs = read(os.path.join("C:/Users/NinaNina/Desktop/Studia!/Inzynierka/proba_mfcc/test", filename))
            norm_sig = sig / max(sig)
            key=filename

            out[key] = mfcc(
                norm_sig,
                fs,
                winlen=0.02,
                numcep=40,
                nfilt=40,
                nfft=int(0.02 * fs),
                highfreq=3000,
                lowfreq=200,
                appendEnergy=False
            )


    return out



def main():
    out=make_mfcc()

    for midi in range(60, 61):
        first_value = False
        mfcc=[]
        for key, element in out.items():

            if int(key[12:14]) == midi:
                if first_value == False:
                    mfcc = out[key]
                    first_value = True
                else:
                    mfcc = concatenate((mfcc, out[key]), axis=0)

        # delta_from_mfcc = delta(mfcc, N=2)
        # delta_delta = delta(delta_from_mfcc, N=2)
        # mfcc = concatenate((mfcc, delta_from_mfcc), axis=1)
        # mfcc = concatenate((mfcc, delta_delta), axis=1)

        print("przelazłem")

        lowest_bic = np.infty
        bic = []
        n_components_range = range(1, 60)
        cv_types = ['spherical', 'tied', 'diag', 'full']
        for cv_type in cv_types:
            for n_components in n_components_range:
                # Fit a Gaussian mixture with EM
                gmm = mixture.GaussianMixture(n_components=n_components,
                                              covariance_type=cv_type)
                gmm.fit(mfcc)
                bic.append(gmm.bic(mfcc))
                if bic[-1] < lowest_bic:
                    lowest_bic = bic[-1]
                    best_gmm = gmm

            print(cv_type,' ',best_gmm)
            plt.plot(bic)
            plt.show()

        # n_components = np.arange(1, 60)
        # models = [mixture.GaussianMixture(n, covariance_type='spherical').fit(mfcc)
        #           for n in n_components]
        #
        # plt.plot(n_components, [m.bic(mfcc) for m in models], label='BIC')
        # #plt.plot(n_components, [m.aic(mfcc) for m in models], label='AIC')
        # plt.legend(loc='best')
        # plt.xlabel('n_components')
        # plt.show()



if __name__ == '__main__':
    main()
