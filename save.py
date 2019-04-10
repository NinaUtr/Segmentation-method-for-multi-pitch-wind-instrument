import threading
import soundfile

class Save(threading.Thread):
    SInstrument=None
    DResults=None
    SPath=None

    def __init__(self,instrument,results,path):
        super(Save,self).__init__()
        self.SInstrument=instrument
        self.DResults=results
        self.SPath=path

    def run(self):
        for key,element in self.DResults.items():
            iteration=0
            for tone in self.DResults[key]:
                song_name=self.SInstrument+'_'+str(tone[1])+'_'+key+'_'+'part'+str(iteration)+'.wav'
                soundfile.write(
                    self.SPath+'/'+song_name,
                    tone[0],
                    tone[2])
                iteration+=1
