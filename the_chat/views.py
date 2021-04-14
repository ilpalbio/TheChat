# librerie di tkinter
import tkinter as tk
from tkinter import ttk
# classi di altri file
from . import widgets as w


'''
classe per i widgets della registrazione
'''

# classe per registrare tutti i widgets
class RecordData(tk.Frame):
    def __init__(self, parent, fields, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # dizionario per tenere traccia di tutti i widgets
        self.inputs = {}

        # aggiunta dei widgets
        # richiesta nome
        self.inputs['Name'] = w.Inputlabel(self, label = 'Name',field_spec = fields['Name'])
        self.inputs['Name'].grid(row = 0, column = 0)

        # richiesta cognome
        self.inputs['Surname'] = w.Inputlabel(self, label = 'Surname', field_spec = fields['Surname'])
        self.inputs['Surname'].grid(row = 1, column = 0)

        # richiesta età
        self.inputs['Age'] = w.Inputlabel(self, 'Age', field_spec = fields['Age'])
        self.inputs['Age'].grid(row = 2, column = 0)

        # richiesta sesso
        self.inputs['Sex'] = w.Inputlabel(self, 'Sex', field_spec = fields['Sex'])
        self.inputs['Sex'].grid(row = 3, column = 0)

        # richiesta Email
        self.inputs['Email'] = w.Inputlabel(self, 'Email',field_spec = fields['Email'])
        self.inputs['Email'].grid(row = 0, column = 1)

        # richiesta passw
        self.inputs['Passwd'] = w.Inputlabel(self, 'Password',field_spec = fields['Passwd'])
        self.inputs['Passwd'].grid(row = 1, column = 1)

        self.reset()

    def get(self):
        data = {}

        for key, widget in self.inputs.items():
            data[key] = widget.get()

        return data

    def reset(self):
        for widget in self.inputs.values():
            widget.set('')
    
    # metodo per restituire gli errori
    def get_errors(self):
        errors = {}
        for key, widget in self.inputs.items():
            if hasattr(widget.input, 'trigger_focusout_validation'):
                widget.input.trigger_focusout_validation()
            if widget.error.get():
                errors[key] = widget.error.get()
        
        return errors
