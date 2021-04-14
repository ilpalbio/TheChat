from .constants import FieldTypes as ft # il punto davanti a constats indica il percorso relativo
import csv
import os

# lista delle età
age = 1900
age_list = []
for i in range(122):
    age_list.append(age)
    age += 1

# classe per i tipi di dato degli input nella registrazione
class CSVModel:
    fields = {
        'Name' : {'req' : True, 'type' : ft.string},
        'Surname' : {'req' : True, 'type' : ft.string},
        'Age' : {'req' : True, 'type' : ft.integer_list, 
            'values' : age_list},

        'Sex' : {'req' : True, 'type' : ft.string_list, 
            'values' : ['Male', 'Female']},

        'Email' : {'req' : True, 'type' : ft.string},
        'Passwd' : {'req' : True, 'type' : ft.string}
    }

    def __init__(self, filename):

        self.filename = filename

    def save_record(self, data):
        # salvataggio dei dati in un file csv
        newfile = not os.path.exists(self.filename)

        with open(self.filename, 'a') as fh:
            csvwriter = csv.DictWriter(fh, fieldnames = self.fields.keys())
            if newfile:
                csvwriter.writeheader()
            csvwriter.writerow(data)
