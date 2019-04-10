import soundfile
import numpy
from recognised_tone import Recognised_Tone
from unrecognised_tone import Unrecognised_Tone

class End_Results:
    DPathMfccs=None
    SInstrument=None
    SPathUnknown=None

    def __init__(self,path_and_mfccs,instrument,path_unknown,callback_progress):
        self.DPathMfccs=path_and_mfccs
        self.SInstrument=instrument
        self.SPathUnknown=path_unknown
        self.CallbackProgress=callback_progress

    def end_result_for_each(self):
        absolute_end_results = {}
        number_of_unknown_songs=len(self.DPathMfccs)
        iteration=0
        for unknown_song in self.DPathMfccs:
            iteration+=1
            self.CallbackProgress(iteration/number_of_unknown_songs)
            for key, element in unknown_song.items():
                path=self.SPathUnknown+"/"+key
                mfcc=element

                out = self.first_counting(mfcc)
                out2 = self.recognised_and_unrecognised_tones(out)
                out3 = self.main_recognition(out2)
                out4 = self.removing_unknown(out3)
                out5 = self.concatenate(out4)

                absolute_end_results[key] = self.end_signals(path,out5)

        return absolute_end_results

    def first_counting(self,mfcc):
        out=[]
        for i in range(len(mfcc)):
            if out==[]:
                out.append([mfcc[i], 1])
            elif mfcc[i]==out[len(out)-1][0]:
                out[len(out)-1][1]=out[len(out)-1][1]+1
            else:
                out.append([mfcc[i], 1])
        return out

    def recognised_and_unrecognised_tones(self,counted_mfcc):
        out = []
        for i in range(numpy.size(counted_mfcc, axis=0)):
            if counted_mfcc[i][1] >= 5:
                out.append(Recognised_Tone(counted_mfcc[i][0], counted_mfcc[i][1]))
            else:
                if len(out) == 0 or isinstance(out[len(out) - 1], Unrecognised_Tone) == False:
                    out.append(Unrecognised_Tone())

                out[len(out) - 1].add_element_in_array(Recognised_Tone(counted_mfcc[i][0], counted_mfcc[i][1]))
        return out

    def main_recognition(self,counted_and_reorganised_mfcc):
        out=counted_and_reorganised_mfcc

        if len(out) > 1:
            for i in range(len(out)):
                element = out[i]

                if isinstance(element, Recognised_Tone):
                    continue

                start_from_right = False
                for unrecognised in element.AUnrecognised:
                    if i==0:
                        out[i + 1].increaseNumberOfRepeats(unrecognised.INumberOfRepeats)
                    elif i==(len(out)-1):
                        out[i - 1].increaseNumberOfRepeats(unrecognised.INumberOfRepeats)
                    else:
                        search_left = self.difference_in_midi(unrecognised.STone, out[i-1].STone)
                        search_right = self.difference_in_midi(unrecognised.STone, out[i+1].STone)
                        if search_left <= search_right and start_from_right == False:
                            out[i-1].increaseNumberOfRepeats(unrecognised.INumberOfRepeats)
                        else:
                            out[i+1].increaseNumberOfRepeats(unrecognised.INumberOfRepeats)
                            start_from_right=True
        return out

    def difference_in_midi(self,known,unknown):
        return abs(int(known) - int(unknown))
    
    def removing_unknown(self,end_mfcc):
        for element in end_mfcc:
            if isinstance(element, Unrecognised_Tone):
                end_mfcc.remove(element)
        return end_mfcc

    def concatenate(self,end_mfcc):
        for i in range(len(end_mfcc)):
            if i < len(end_mfcc)-1 and end_mfcc[i].STone==end_mfcc[i+1].STone:
                end_mfcc[i+1].increaseNumberOfRepeats(end_mfcc[i].INumberOfRepeats)
                end_mfcc.remove(end_mfcc[i])
        return end_mfcc

    def end_signals(self,path,recognition):
        sig, fs = soundfile.read(path)

        dt = 1 / fs
        end_of_first_midi = 0
        signals=[]
        for element in recognition:
            samples_per_midi = int((0.035 * element.INumberOfRepeats) / dt)
            end = end_of_first_midi + samples_per_midi

            signal_per_midi = sig[end_of_first_midi:end]
            end_of_first_midi = end_of_first_midi + samples_per_midi

            signals.append([signal_per_midi,element.STone,fs])
        return signals