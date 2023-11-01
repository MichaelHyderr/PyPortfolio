class Outcome:
    def __init__(self):
        self.status = None
        self.google = None
        self.json = None
        self.row = None

    def __str__(self): # quando chiami print(outcome), il metodo __str__  viene eseguito e restituisce una stringa che descrive l'oggetto
        details = ''
        details += f'Status           : {self.status}\n\n'
        details += f'Google Result    : {self.google}\n\n'
        if self.json is not None:
            details += f'Sheet Json       : {self.json}\n\n'
        if self.row is not None:
            details += f'New Row          : {self.row}\n\n'
        return details

    def google_to_json(self):  # in caso di "read" converto il result del metodo di google in un json per analizzare il contenuto
        google_sheet_list = self.google["values"]
        google_sheet_json = {title: [] for title in google_sheet_list[0]}

        for n in range(len(list(google_sheet_json.keys()))):
            for nested_list in google_sheet_list[1:]:
                try:
                    google_sheet_json[list(google_sheet_json.keys())[n]].append(nested_list[n])
                except IndexError:
                    google_sheet_json[list(google_sheet_json.keys())[n]].append("")

        return google_sheet_json

