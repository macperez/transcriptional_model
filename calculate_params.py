import gspread
from utils import DataSheet
from utils import SearchInColumns
from oauth2client.service_account import ServiceAccountCredentials


NUCLEOTID_COL = 1
SEQUENCE_COL = 2
NUCLEOTID_ROW_INIT = 3
NUCLEOTID_ROW_END = 282


def compute_tscr_elo_term_TU0_xxxx(sheet):
    datos_sh = sheet.data_sheet
    nucleotid_seq_sh = sheet.parent.worksheet('Secuencia nucleotidica')
    mRNA_list = datos_sh.range('AO4:AO8')
    search = SearchInColumns(nucleotid_seq_sh,'A3:A282')
    search.look_for(datos_sh, 'AO4:AO8')
    results = search.get_values('B')
    atp = sum((seq.count('A') for seq in results))
    print(atp)


def look_nucleotid_seq(nucleotid_names, mRNA, is_sorted=False):
        index = NUCLEOTID_ROW_INIT
        if not is_sorted:
            for n in nucleotid_names:
                if mRNA == n:
                    break
                index += 1
        return index


def main():
    scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('transcriptional-model-key.json', scope)

    gc = gspread.authorize(credentials)
    # Open a worksheet from spreadsheet with one shot
    spreadsheet = gc.open("ematix_05_10")
    wk = spreadsheet.worksheet('Datos')
    sheet = DataSheet(spreadsheet, wk)
    compute_tscr_elo_term_TU0_xxxx(sheet)
    # wks.update_acell('B2', "it's down there somewhere, let me take another look.")

    # Fetch a cell range
    # cell_list = wks.range('A1:B7')
    # print(cell_list)



if __name__ == '__main__':
    main()
