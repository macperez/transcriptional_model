import gspread
from oauth2client.service_account import ServiceAccountCredentials



def main():
    scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('transcriptional-model-key.json', scope)

    gc = gspread.authorize(credentials)
    # Open a worksheet from spreadsheet with one shot
    wks = gc.open("ematix_05_10").sheet1

    # wks.update_acell('B2', "it's down there somewhere, let me take another look.")

    # Fetch a cell range
    cell_list = wks.range('A1:B7')
    print(cell_list)

if __name__ == '__main__':
    main()
