import gspread
from oauth2client.service_account import ServiceAccountCredentials


NUCLEOTID_COL = 1
SEQUENCE_COL = 2
NUCLEOTID_ROW_INIT = 3
NUCLEOTID_ROW_END = 282


def compute_tscr_elo_term_TU0_xxxx(sheet, worksheet):
    datos_sh = sheet.worksheet('Datos')
    nucleotid_seq_sh = sheet.worksheet('Secuencia nucleotidica')
    mRNA_list = datos_sh.range('AO4:AO8')
    nucleotid_names = [cell.value for cell in nucleotid_seq_sh.range(
        NUCLEOTID_ROW_INIT, NUCLEOTID_COL,
        NUCLEOTID_ROW_END, NUCLEOTID_COL
    )]
    atps = []
    for mRNA_cell in mRNA_list:
        mRNA = mRNA_cell.value
        row = look_nucleotid_seq(nucleotid_names, mRNA)
        seq = nucleotid_seq_sh.cell(row, SEQUENCE_COL).value
        atp = seq.count('A')
        atps.append(atp)
    print(atps)


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
    sheet = gc.open("ematix_05_10")
    wk = sheet.worksheet('Datos')
    compute_tscr_elo_term_TU0_xxxx(sheet, wk)
    # wks.update_acell('B2', "it's down there somewhere, let me take another look.")

    # Fetch a cell range
    # cell_list = wks.range('A1:B7')
    # print(cell_list)



if __name__ == '__main__':
    main()
