from __future__ import print_function  # __future__ permette di utilizzare print_function delle versioni future di python con qualunque modifica essa abbia

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_sheets_outcome import Outcome


class GoogleSheetAPI:
    """
    Define spreadsheet : Open your spreadsheet on the browser and copy the id from the url
    Define range_name : Identify the area where you want to edit your sheet, If only 1 table, just insert the sheet name, e.g. "sheet1",
    for more info go to https://developers.google.com/sheets/api/guides/values\n
    Define values : if execute_google_method(purpose!="read"), Values must be entered in the following format: [ ['a','b','c'], ['d','e','f'] ]
    """

    def __init__(self):
        self.scope = ['https://www.googleapis.com/auth/spreadsheets']
        self.spreadsheet = None
        self.range_name = None
        self.values = None
        self.value_input_option = "RAW"  # Con RAW L'input non viene analizzato e viene inserito come stringa. Ad esempio, l'input "=1+2" inserisce la stringa, non la formula, "=1+2" nella cella.

    def execute_google_method(self, purpose):
        """
        :param purpose: can be : "append", "read", "update"
        :return: the corresponding Google method for the intended purpose and execute it
        """

        creds = self.get_creds()
        outcome = Outcome()

        if purpose == "append":
            result = self.append_values(self.spreadsheet, self.range_name, self.value_input_option, self.values, creds)  # popola il metodo di google
            if "HttpError" in str(result):  # se nel risultato è presente quella stringa allora c'è stato un errore
                outcome.status = "KO"
                outcome.google = result
            else:
                outcome.status = "OK"
                outcome.google = result
                outcome.row = self.values

        elif purpose == "read":
            result = self.get_values(self.spreadsheet, self.range_name, creds)
            if "HttpError" in str(result):
                outcome.status = "KO"
                outcome.google = result
            else:
                outcome.status = "OK"
                outcome.google = result
                outcome.json = outcome.google_to_json()

        elif purpose == "update":
            result = self.update_values(self.spreadsheet, self.range_name, self.value_input_option, self.values, creds)
            if "HttpError" in str(result):
                outcome.status = "KO"
                outcome.google = result
            else:
                outcome.status = "OK"
                outcome.google = result
                outcome.row = self.values

        else:
            outcome.status = "KO"
            outcome.google = "Wrong purpose, You can only type 'read','append' or 'update'"

        return outcome

    def get_creds(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token_spreadsheet.json'):
            creds = Credentials.from_authorized_user_file('token_spreadsheet.json', self.scope)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            # le 3 righe sotto vanno attivate nel caso l'app su google cloud passa da test a operativa, da flow in sotto va indentato a destra
            # if creds and creds.expired and creds.refresh_token:
            #     creds.refresh(Request())
            #     return creds
            # else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', self.scope)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token_spreadsheet.json', 'w') as token:
            token.write(creds.to_json())
        return creds


    def get_values(self, spreadsheet_id: str, range_name: str, creds: dict):
        """
        :param spreadsheet_id: from the sheet URL
        :param range_name: where you want to operate see table https://developers.google.com/sheets/api/guides/values
        :param creds: passed from main(), token
        :return: read the spreadsheet
        """
        try:
            service = build('sheets', 'v4', credentials=creds)

            result = service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id, range=range_name).execute()
            return result

        except HttpError as error:
            print(f"An error occurred: {error}")
            return error


    def append_values(self, spreadsheet_id: str, range_name: str, value_input_option: str, values: list, creds: dict):
        """
        :param spreadsheet_id: from the sheet URL
        :param range_name: where you want to operate see table https://developers.google.com/sheets/api/guides/values
        :param value_input_option: either "RAW"(default) or "USER_ENTERED", see https://developers.google.com/sheets/api/guides/values
        :param values: what you need to add into the sheet
        :param creds: passed from execute_google_method()
        :return: adds values
        """
        try:
            service = build('sheets', 'v4', credentials=creds)

            body = {'values': values}

            result = service.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                body=body
            ).execute()
            return result

        except HttpError as error:
            return error

    def update_values(self, spreadsheet_id, range_name, value_input_option, values, creds):
        """
        :param spreadsheet_id: from the sheet URL
        :param range_name: where you want to operate see table https://developers.google.com/sheets/api/guides/values
        :param value_input_option: either "RAW"(default) or "USER_ENTERED", see https://developers.google.com/sheets/api/guides/values
        :param values: what you want to enter into the sheet
        :param creds: passed from main(), token
        :return: updates values to range_name cells
        """
        try:
            service = build('sheets', 'v4', credentials=creds)

            body = {
                'values': values
            }
            result = service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                body=body
            ).execute()
            return result

        except HttpError as error:
            print(f"An error occurred: {error}")
            return error
