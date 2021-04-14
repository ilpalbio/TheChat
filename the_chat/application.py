# importazione delle librerie di tkinter
import tkinter as tk
from tkinter import ttk
# librerie per la data
from datetime import datetime
# librerie di altri file
from . import views as v
from . import models as m

# classe per la registrazione
class Registration(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title('TheChat')
        self.geometry('400x300')
        self.resizable(width = False, height = False)

        ttk.Label(self, text = 'TheChat', font = ('TkDefaultFont', 16)).grid(row = 0, column = 0)
         
        # aggiunta dei widgets in RecordDAta
        self.recordata = v.RecordData(self, m.CSVModel.fields)
        self.recordata.grid(row = 1, column = 0, padx = 10) # padx serve per l'interlinea tra i widgets

        # aggiunta del bottone per registrarsi
        self.save = ttk.Button(self, text = 'Registrati', command = self.on_save)
        self.save.grid(row = 4, column = 1, sticky = tk.E)

    def on_save(self): # funzione per salvare i dati della registrazione
        # controllo se ci sono degli errori
        errors = self.recordata.get_errors()
        if errors:
            return False

        datestring = datetime.today().strftime('%y-%m-%d') # formattazione dell'orario
        filename = 'TheChat_record_data_{}.csv'.format(datestring)
        model = m.CSVModel(filename)
           
        # presa delle informazioni
        data = self.recordata.get()

        # Salvataggio dei dati in un file
        datestring = datetime.today().strftime("%Y-%m-%d")
        filename = "abq_data_record_{}.csv".format(datestring)
        model = m.CSVModel(filename)
        data = self.recordform.get()
        model.save_record(data)

        self.recordform.reset()


