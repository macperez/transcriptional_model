import gspread
from utils import DataSheet
from utils import SearchInColumns
from oauth2client.service_account import ServiceAccountCredentials

ATP_COL = 19
H_COL = 26
MRNA_ROW_END = 285

# (4, 49, 282, 70) == AW4:BR285
TL_ELO_XXXX_1_RIB1_FIRST_ROW = 4
TL_ELO_XXXX_1_RIB1_LAST_ROW = 285
TL_ELO_XXXX_1_RIB1_FIRST_COL = 49
TL_ELO_XXXX_1_RIB1_LAST_COL = 70

# (4, 71, 4, 96) == BS4:CR285
TL_ELO_XXXX_1_RIB2_FIRST_ROW = 4
TL_ELO_XXXX_1_RIB2_LAST_ROW = 285
TL_ELO_XXXX_1_RIB2_FIRST_COL = 71
TL_ELO_XXXX_1_RIB1_LAST_COL = 96



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



def calculate_tl_elo_xxxx_1_rib1(sheet):
    tu_rows, end_ranges = get_tu_limits(sheet)
    amino_seq_sh = sheet.parent.worksheet('Secuencia aminoacidica')
    searcher = SearchInColumns(amino_seq_sh, 'A3:B282', 1)
    datos_sh = sheet.data_sheet
    searcher.preload_cells(datos_sh, 'AM4:AM285')
    results = searcher.search(TL_ELO_XXXX_1_RIB1_FIRST_ROW,
                              TL_ELO_XXXX_1_RIB1_LAST_ROW)
    computation_cell_range = datos_sh.range('AW4:BR285')
    index = 0
    for gen_seq in results:
        # first col
        seq = gen_seq
        efg_gtp = len(seq)
        computation_cell_range[index].value = efg_gtp
        index += 1
        # letters cols
        for letter in 'ARNDEGHILKMFPSTYVCWQ':
            computation_cell_range[index].value = seq.count(letter)
            index += 1
        # last col
        computation_cell_range[index].value = efg_gtp*3
        index += 1
    datos_sh.update_cells(computation_cell_range)


def calculate_tl_elo_xxxx_1_rib2(sheet):
    """
    Very similar to calculate_tl_elo_xxxx_1_rib1 but if the sequence ends
    with an specific letter then column that contains this summatory less one.
    """
    tu_rows, end_ranges = get_tu_limits(sheet)
    amino_seq_sh = sheet.parent.worksheet('Secuencia aminoacidica')
    searcher = SearchInColumns(amino_seq_sh, 'A3:B282', 1)
    datos_sh = sheet.data_sheet
    searcher.preload_cells(datos_sh, 'AM4:AM285')
    crowed_results = searcher.search(TL_ELO_XXXX_1_RIB2_FIRST_ROW,
                                     TL_ELO_XXXX_1_RIB2_LAST_ROW)
    results = [seq.strip() for seq in crowed_results]
    computation_cell_range = datos_sh.range('BS4:CR285')
    name_cols = ['ala1', 'arg1', 'asn1', 'asp1', 'glu1', 'gly1', 'hisR',
                 'ile1', 'leu1', 'lys1', 'met1', 'phe1', 'pro1', 'ser1', 'thr1',
                 'tyr1', 'val1', 'cys', 'trp', 'gln']
    letters = 'ARNDEGHILKMFPSTYVCWQ'
    mapping_cols = dict(zip(letters, name_cols))
    values_to_update_in_col_CZ = []
    index = 0
    import ipdb; ipdb.set_trace()
    for gen_seq in results:
        # first three cols
        if gen_seq is None or gen_seq == '':
            values_to_update_in_col_CZ.append('##')
            continue
        last_letter = gen_seq[-1]
        values_to_update_in_col_CZ.append(mapping_cols[last_letter])
        seq = gen_seq[:-1]  # remove the last letter in seq
        h2o = len(seq)
        ef_g_gdp = h2o
        ef_tu_gdp = h2o
        computation_cell_range[index].value = h2o
        index += 1
        computation_cell_range[index].value = ef_g_gdp
        index += 1
        computation_cell_range[index].value = ef_tu_gdp
        index += 1
        # letters cols
        for letter in 'ARNDEGHILKMFPSTYVCWQ':
            computation_cell_range[index].value = seq.count(letter)
            index += 1
        # last three cols
        mg2 = ef_g_gdp * 5
        computation_cell_range[index].value = mg2
        index += 1
        pi = h2o * 2
        computation_cell_range[index].value = pi
        index += 1
        h = h2o * 2
        computation_cell_range[index].value = pi
        index += 1

    # datos_sh.update_cells(computation_cell_range)

    ## Now we update the CZ col: tRNA
    computation_cell_range = datos_sh.range('CZ4:CZ285')
    index = 0
    for el in values_to_update_in_col_CZ:
        computation_cell_range[index].value = el
        index += 1

    datos_sh.update_cells(computation_cell_range)


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
    # calculate_tl_elo_xxxx_1_rib1(sheet)
    calculate_tl_elo_xxxx_1_rib2(sheet)

if __name__ == '__main__':
    # main()
    print("Deactivated .. module")
