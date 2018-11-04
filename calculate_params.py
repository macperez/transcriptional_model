import gspread
from utils import DataSheet
from utils import SearchInColumns
from oauth2client.service_account import ServiceAccountCredentials



ATP_COL = 19
H_COL = 26
MRNA_ROW_END = 285


def compute_tscr_elo_term_TU0_xxxx(sheet):
    datos_sh = sheet.data_sheet
    nucleotid_seq_sh = sheet.parent.worksheet('Secuencia nucleotidica')
    search = SearchInColumns(nucleotid_seq_sh, 'A3:A282')
    search.look_for(datos_sh, 'AO4:AO8')
    results = search.get_values('B')
    atp = sum((seq.count('A') for seq in results))
    print(atp)


def calculate_tscr_elo_term_TUB0_xxxx(sheet):
    datos_sh = sheet.data_sheet
    tu_rows = []
    for cell in datos_sh.range('A4:A282'):
        if 'TU_' in cell.value.upper():
            tu_rows.append(cell.row)
    end_ranges = [row - 1 for row in tu_rows]
    end_ranges = end_ranges[1:]
    end_ranges.append(MRNA_ROW_END)
    nucleotid_seq_sh = sheet.parent.worksheet('Secuencia nucleotidica')
    searcher = SearchInColumns(nucleotid_seq_sh, 'A3:B282', 1)
    searcher.preload_cells(datos_sh, 'AM4:AM285')
    for init, end in zip(tu_rows, end_ranges):
        results = searcher.search(init, end)
        atp = sum((seq[1].count('A') for seq in results))
        ctp = sum((seq[1].count('C') for seq in results))
        gtp = sum((seq[1].count('G') for seq in results))
        utp = sum((seq[1].count('T') for seq in results))
        ppi = atp + ctp + gtp + utp
        row_cell_list = datos_sh.range(init, ATP_COL, init, H_COL)
        row_cell_list[0].value = atp
        row_cell_list[1].value = ctp
        row_cell_list[2].value = gtp
        row_cell_list[3].value = utp
        row_cell_list[4].value = ppi
        row_cell_list[5].value = 3
        row_cell_list[6].value = 3
        row_cell_list[7].value = 3
        datos_sh.update_cells(row_cell_list)
        print('From row {} to row {}'.format(init, end))


def main():
    scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('transcriptional-model-key.json', scope)

    gc = gspread.authorize(credentials)
    # Open a worksheet from spreadsheet with one shot
    spreadsheet = gc.open("ematix_05_10")
    wk = spreadsheet.worksheet('Datos')
    sheet = DataSheet(spreadsheet, wk)
    # compute_tscr_elo_term_TU0_xxxx(sheet)
    calculate_tscr_elo_term_TUB0_xxxx(sheet)
    # wks.update_acell('B2', "it's down there somewhere, let me take another look.")
    # Fetch a cell range
    # cell_list = wks.range('A1:B7')
    # print(cell_list)


if __name__ == '__main__':
    main()
