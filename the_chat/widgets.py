# moduli di tkinter
import tkinter as tk
from tkinter import ttk
# importazioni di file
from .constants import FieldTypes as ft


'''
classi per convalidare gli input
'''
class ValidateMixin:
    def __init__(self, *args, error_var = None, **kwargs):
        self.error = error_var or tk.StringVar()
        super().__init__(*args, **kwargs)
        
        # convalidazione
        vcmd = self.register(self._validate)
        invcmd = self.register(self._invalid)
        self.config(validate = 'all', 
        validatecommand = (vcmd, '%P', '%s', '%S', '%V', '%i', '%d'),
        invalidcommand = (invcmd, '%P', '%s', '%S', '%V', '%i', '%d'))

    # metodo per il colore dell'errore
    def _toggle_error(self, on = False):
        self.config(foreground = ('red' if on else 'black'))

    # metodo per la convalidazione dell'input
    def _validate(self, proposed, current, char, event, index, action):
        self._toggle_error(False)
        self.error.set('')
        valid = True

        if event == 'focusout':
            valid = self._focusout_validate(event = event)

        elif event == 'key':
            valid = self._key_validate(
            proposed = proposed, current = current, char = char, event = event, index = index, action = action)

        return valid

    # metodo per event = focusout
    def _focusout_validate(self, **kwargs):
        return True

    # metodo per event = key
    def _key_validate(self, **kwargs):
        return True

    # meodo per la invalidazione dell'input
    def _invalid(self, proposed, current, char, event, index, action):
        if event == 'focusout':
            self._focusout_invalid(event = event)

        elif event == 'key':
            self._key_invalid(
            proposed = proposed, current = current, char = char, event = event, index = index, action = action
            )

    def _focusout_invalid(self, **kwargs):
        self._toggle_error(True)

    def _key_invalid(self, **kwargs):
        pass

    # metodo che attia la focusout_validation
    def trigger_focusout_validation(self):
        valid = self._validate('', '', '', 'focusout', '', '')
        if not valid:
            self._focusout_invalid(event = 'focusout')

        return valid

# classe per fare in modo che tutti gli Entry siano soddisfatti
class RequiredEntry(ValidateMixin, ttk.Entry):
    def _focusout_validate(self, event):
        valid = True
        if not self.get():
            valid = False
            self.error.set('A value is required')

        return valid

# classe per convalidare gli input nei ComboBox
class ValidatedCombobox(ValidateMixin, ttk.Combobox):
    def _key_validate(self, proposed, action, **kwargs):
        valid = True
        
        # se l'utente prova ad eliminare quello che ha scritto si elimina tutta la riga
        if action == '0':
            self.set('')
            return True

        # parte in cui viene proposta la risposta all'utente
        # lista dei valori
        values = self.cget('values')
        
        matching = [
            x for x in values
                if x.lower().startswith(proposed.lower())
        ]

        if len(matching) == 0: # se la lunghezza di matching è uguale a 0 non c'è  nessun valore
            valid = False

        elif len(matching) == 1: # se la lunghezza è 1 è stato trovato un elemento
            self.set(matching[0])
            self.icursor(tk.END)

        return valid

    def _focusout_validate(self, **kwargs):
        valid = True
        if not self.get():
            valid = False
            self.error.set('A value is required')

        return valid

'''
classe per semplificare la scrittura dei widgets
'''
class Inputlabel(tk.Frame):
    field_types = {
        ft.string : (RequiredEntry, tk.StringVar),
        ft.string_list : (ValidatedCombobox, tk.StringVar),
        ft.integer_list : (ValidatedCombobox, tk.IntVar),
        ft.boolean : (ttk.Checkbutton, tk.BooleanVar)
    }

    # costruttore
    def __init__(self, parent, label = '', input_class = None,
                 input_var = None, input_args = None, label_args = None, 
                 field_spec = None ,**kwargs):

        super().__init__(parent, **kwargs)
        input_args = input_args or {}
        label_args = label_args or {}

        if field_spec:
            field_type = field_spec.get('type', ft.string)
            input_class = input_class or self.field_types.get(field_type)[0]
            var_type = self.field_types.get(field_type)[1]
            self.variable = input_var if input_var else var_type()
            # values
            if 'values' in field_spec and 'values' not in input_args:
                input_args['values'] = field_spec.get('values')

        else:
            self.variable = input_var

        if input_class in (ttk.Checkbutton, ttk.Button, ttk.Radiobutton):
            input_args["text"] = label
            input_args["variable"] = self.variable
        else:
            self.label = ttk.Label(self, text=label, **label_args)
            self.label.grid(row=0, column=0, sticky=(tk.W + tk.E))
            input_args["textvariable"] = self.variable

        self.input = input_class(self, **input_args)
        self.input.grid(row=1, column=0, sticky=(tk.W + tk.E))
        self.columnconfigure(0, weight=1)

        self.error = getattr(self.input, 'error', tk.StringVar())
        self.error_label = ttk.Label(self, textvariable = self.error)
        self.error_label.grid(row = 2, column = 0, sticky = (tk.W, tk.E))

    def grid(self, sticky=(tk.E + tk.W), **kwargs):
        super().grid(sticky=sticky, **kwargs)

    def get(self):
        if self.variable:
            return self.variable.get()
        elif type(self.input) == tk.Text:
            return self.input.get('1.0', tk.END)
        else:
            return self.input.get()

    def set(self, value, *args, **kwargs):
        if type(self.variable) == tk.BooleanVar:
                self.variable.set(bool(value))
        elif self.variable:
                self.variable.set(value, *args, **kwargs)
        elif type(self.input).__name__.endswith('button'):
            if value:
                self.input.select()
            else:
                self.input.deselect()
        elif type(self.input) == tk.Text:
            self.input.delete('1.0', tk.END)
            self.input.insert('1.0', value)
        else:
            self.input.delete(0, tk.END)
            self.input.insert(0, value)
