import gspread
from utils import DataSheet
from utils import SearchInColumns
from oauth2client.service_account import ServiceAccountCredentials

ATP_COL = 19
H_COL = 26
MRNA_ROW_END = 285


def calculate_tscr_elo_term_TUB0_xxxx(sheet):
    tu_rows, end_ranges = get_tu_limits(sheet)
    nucleotid_seq_sh = sheet.parent.worksheet('Secuencia nucleotidica')
    searcher = SearchInColumns(nucleotid_seq_sh, 'A3:B282', 1)
    datos_sh = sheet.data_sheet
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


def calculate_tl_elo_xxxx_1_rib1(sheet):
    tu_rows, end_ranges = get_tu_limits(sheet)
    amino_seq_sh = sheet.parent.worksheet('Secuencia aminoacidica')
    searcher = SearchInColumns(amino_seq_sh, 'A3:B282', 1)
    datos_sh = sheet.data_sheet
    searcher.preload_cells(datos_sh, 'AM4:AM285')
    computation_cell_range = datos_sh.range('AW4:BR282')
    import ipdb; ipdb.set_trace()
    for init, end in zip(tu_rows, end_ranges):
        index = 0
        results = searcher.search(init, end)
        for letter in 'ARNDEGHILKMFPSTYVCWQA':
           pep = sum((seq[1].count(letter) for seq in results))
           
        

def get_tu_limits(sheet):
    datos_sh = sheet.data_sheet
    tu_rows = []
    for cell in datos_sh.range('A4:A282'):
        if 'TU_' in cell.value.upper():
            tu_rows.append(cell.row)
    end_ranges = [row - 1 for row in tu_rows]
    end_ranges = end_ranges[1:]
    end_ranges.append(MRNA_ROW_END)

    return tu_rows, end_ranges


def main():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.\
        from_json_keyfile_name('transcriptional-model-key.json', scope)
    gc = gspread.authorize(credentials)
    spreadsheet = gc.open("ematix_05_10")
    wk = spreadsheet.worksheet('Datos')
    sheet = DataSheet(spreadsheet, wk)
    # calculate_tscr_elo_term_TUB0_xxxx(sheet)
    calculate_tl_elo_xxxx_1_rib1(sheet)

if __name__ == '__main__':
    main()
