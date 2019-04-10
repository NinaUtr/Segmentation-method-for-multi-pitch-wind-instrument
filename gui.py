from ttkthemes import themed_tk as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from analyze import Analyze
from save import Save
from top_level_window import Top_Level_Window
import os

class Gui:

    SPathUnknown=None
    SPathForSaving=None
    SInstrument=None
    root=None

    instrumentVar=None
    listVar = None
    saveVar = None
    restartVar=None

    SText=None
    SText2=None
    resultList=None
    saveButton=None

    DEndResults=None

    def browse_file(self):
        self.SText.delete('1.0', END)
        self.SPathUnknown = filedialog.askdirectory()
        self.SText.insert(INSERT, self.SPathUnknown)

    def browse_file_for_saving(self):
        self.SText2.delete('1.0', END)
        self.SPathForSaving = filedialog.askdirectory()
        self.SText2.insert(INSERT, self.SPathForSaving)

    def choose_instrument(self):
        if self.instrumentVar.get() == 1:
            self.SInstrument = "flute"
        elif self.instrumentVar.get() == 2:
            self.SInstrument = "oboe"
        elif self.instrumentVar.get() == 3:
            self.SInstrument = "clarnet"

    def activate_list(self):
        if self.listVar.get()==1:
            self.resultList.config(state=NORMAL)

        elif self.listVar.get()==0:
            self.resultList.config(state=DISABLED)

    def activate_save(self):
        if self.saveVar.get()==1:
            self.saveButton.config(state=NORMAL)
            self.SText2.config(state=NORMAL)

        elif self.saveVar.get()==0:
            self.saveButton.config(state=DISABLED)
            self.SText2.config(state=DISABLED)

    def progress_bar(self,progress):
        self.ProgressVar.set(progress)

    def analyze(self):
        self.ProgressVar.set(0)
        if self.SPathUnknown==None or self.SInstrument==None or (self.saveVar.get()==1 and self.SPathForSaving==None):
            messagebox.showerror('Ojej! Wystąpił błąd.','Nie podano ścieżki do plików bądź nie wybrano instrumentu!')
        elif self.restartVar==None:
            action=Analyze(self.SInstrument,self.SPathUnknown,callback=self.results,callback_progress=self.progress_bar)
            action.start()
            self.restartVar==self.SInstrument
        else:
            if os.path.exists('mfcc/mfccs_unknown_' + self.restartVar + '.p'):
                os.remove('mfcc/mfccs_unknown_' + self.restartVar + '.p')
            action = Analyze(self.SInstrument, self.SPathUnknown, callback=self.results,callback_progress=self.progress_bar)
            action.start()

    def results(self,end_results):
        self.DEndResults=end_results
        if self.listVar.get()==1:
            iteration = 0
            for key, element in end_results.items():
                self.resultList.insert(iteration, key)
                iteration += 1

        if self.saveVar.get()==1:
            saving=Save(self.SInstrument,self.DEndResults,self.SPathForSaving)
            saving.start()

    def on_double_click(self, event):
        if self.resultList.size()!=0:
            widget = event.widget
            selection = widget.curselection()
            song_name = widget.get(selection[0])
            Top_Level_Window(song_name,self.DEndResults[song_name])

    def clear(self):
        self.resultList.delete(0, END)

    def ask_quit(self):
        if not self.SInstrument==None:
            if os.path.exists('mfcc/mfccs_unknown_'+self.SInstrument+'.p'):
                os.remove('mfcc/mfccs_unknown_'+self.SInstrument+'.p')
        self.root.destroy()



    def initialise_application(self):
        self.root = tk.ThemedTk()
        self.root.get_themes()
        self.root.set_theme("equilux")
        self.root.geometry('950x600')
        # self.root.iconbitmap()
        self.root.title("Melody")
        self.root.configure(bg="#424242")
        self.root.protocol("WM_DELETE_WINDOW", self.ask_quit)

        # wybor sciezki do nieznanych utworow
        searchFrame=ttk.Frame(self.root)
        searchFrame.place(height=150, width=400, x=50, y=50)

        searchText = """Podaj ścieżkę do folderu z nagraniami,
które chcesz analizować:"""

        searchLabel = ttk.Label(searchFrame, text=searchText,justify=LEFT)
        searchLabel.pack()
        searchLabel.place(bordermode=INSIDE, height=50, width=250, x=25, y=12)

        searchButton = ttk.Button(searchFrame, text="Szukaj", command=self.browse_file)
        searchButton.pack()
        searchButton.place(bordermode=INSIDE,height=50,width=75,x=300,y=75)

        self.SText = Text(searchFrame)
        self.SText.pack()
        self.SText.place(bordermode=INSIDE,height=50,width=250,x=25,y=75)

        # wybor instrumentu
        self.instrumentVar = IntVar()

        instrumentFrame = ttk.Frame(self.root)
        instrumentFrame.place(height=125, width=400, x=50, y=225)

        instrumentText = """Wybierz instrument, którego nagrania 
chcesz analizować:"""

        instrumentLabel = ttk.Label(instrumentFrame, text=instrumentText, justify=LEFT)
        instrumentLabel.pack()
        instrumentLabel.place(bordermode=INSIDE, height=50, width=400, x=25, y=12)

        flute = ttk.Radiobutton(instrumentFrame , text="Flet", variable=self.instrumentVar, value=1, command=self.choose_instrument)
        flute.pack()
        flute.place(bordermode=INSIDE, height=30, width=100, x=25, y=75)

        oboe = ttk.Radiobutton(instrumentFrame , text="Obój", variable=self.instrumentVar, value=2, command=self.choose_instrument)
        oboe.pack()
        oboe.place(bordermode=INSIDE, height=30, width=100, x=150, y=75)

        clarnet = ttk.Radiobutton(instrumentFrame , text="Klarnet", variable=self.instrumentVar, value=3, command=self.choose_instrument)
        clarnet.pack()
        clarnet.place(bordermode=INSIDE, height=30, width=100, x=275, y=75)

        #pokazywanie wynikow
        self.listVar = IntVar()
        self.listVar.set(1)

        resultFrame = ttk.Frame(self.root)
        resultFrame.place(height=500, width=400, x=500, y=50)

        analyzeButton = ttk.Button(resultFrame, text="Analizuj", command=self.analyze)
        analyzeButton.pack()
        analyzeButton.place(bordermode=INSIDE, height=75, width=350, x=25, y=50)

        self.ProgressVar = IntVar()
        self.progressBar = ttk.Progressbar(resultFrame, maximum=1, variable=self.ProgressVar, orient=HORIZONTAL)
        self.progressBar.pack()
        self.progressBar.place(bordermode=INSIDE, height=10, width=350, x=25, y=25)

        clearButton = ttk.Button(resultFrame, text="Wyczyść listę", command=self.clear)
        clearButton.pack()
        clearButton.place(bordermode=INSIDE, height=30, width=150, x=225, y=135)

        resultButton=ttk.Checkbutton(resultFrame, text="Pokaż wyniki",variable=self.listVar, command=self.activate_list)
        resultButton.pack()
        resultButton.place(bordermode=INSIDE, height=50, width=150, x=25, y=125)

        self.resultList = Listbox(resultFrame)
        self.resultList.bind("<Double-Button-1>", self.on_double_click)
        self.resultList.pack()
        self.resultList.place(bordermode=INSIDE, height=300, width=350, x=25, y=175)

        scrollbar = Scrollbar(self.resultList, orient="vertical")
        scrollbar.config(command=self.resultList.yview)
        scrollbar.pack(side="right", fill="y")

        self.resultList.config(yscrollcommand=scrollbar.set)

        # zapisywanie wynikow do folderu
        self.saveVar = IntVar()
        self.saveVar.set(0)

        saveFrame = ttk.Frame(self.root)
        saveFrame.place(height=175, width=400, x=50, y=375)

        saveText = """Podaj ścieżkę do folderu, gdzie mają 
zostać zapisane pocięte pliki:"""

        saveLabel = ttk.Label(saveFrame, text=saveText, justify=LEFT)
        saveLabel.pack()
        saveLabel.place(bordermode=INSIDE, height=50, width=250, x=25, y=40)

        saveCheckbutton = ttk.Checkbutton(saveFrame, text="Zapisz wyniki", variable=self.saveVar, command=self.activate_save)
        saveCheckbutton.pack()
        saveCheckbutton.place(bordermode=INSIDE, height=30, width=300,x=25,y=10)

        self.saveButton = ttk.Button(saveFrame, text="Szukaj", command=self.browse_file_for_saving)
        self.saveButton.config(state=DISABLED)
        self.saveButton.pack()
        self.saveButton.place(bordermode=INSIDE,height=50,width=75,x=300,y=100)

        self.SText2 = Text(saveFrame)
        self.SText2.config(state=DISABLED)
        self.SText2.pack()
        self.SText2.place(bordermode=INSIDE, height=50,width=250,x=25,y=100)



        self.root.mainloop()

