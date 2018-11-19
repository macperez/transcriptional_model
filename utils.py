import sys


class DataSheet():
    def __init__(self, spreadsheet, wk):
        self.data_sheet = wk
        self.parent = spreadsheet


class SearchInColumns():
    def __init__(self, base_datasheet, base_range, key_column):
        sq_dimensions = get_square_coordinates(base_range)
        self.key_column = key_column
        self.datasheet_in = base_datasheet
        self.init_row = sq_dimensions[0]
        self.init_col = sq_dimensions[1]
        self.end_row = sq_dimensions[2]
        self.end_col = sq_dimensions[3]
        rng_sht = base_datasheet.range(self.init_row, self.init_col,
                                       self.end_row, self.end_col)
        self.base_cells = self._convert_to_dict(rng_sht)
        self.cells = None
        self.results = None

    def _convert_to_dict(self, sh_range):
        if self.end_col > 2:
            raise Exception('Incorrect format to use SearchInColumns')
        info = {}
        for cell_key, cell_value in zip(sh_range[::2], sh_range[1::2]):
            info[cell_key.value.upper()] = (cell_key, cell_value.value)
        return info

    def preload_cells(self, datasheet, search_range):
        self.cells = [cell for cell in datasheet.range(search_range)
                      if cell.value != '']

    def search(self, init, end, same_arrangement=True):
        result = []
        for cell in self.cells:
            if cell.row >= init and cell.row <= end:
                if self.base_cells[cell.value.upper()] != '':
                    result.append(self.base_cells[cell.value.upper()])
        return result


def extract_coordinates(col_row_notation='JK288'):
    letters = []
    numbers = []
    for ch in col_row_notation:
        if ch.isdigit():
            numbers.append(ch)
        else:
            letters.append(ch)
    return ''.join(letters).upper(), int(''.join(numbers))


def column(cadena):
    col = 0
    if len(cadena) > 1:
        for let in cadena[-2]:
            col += 26*(ord(let) - ord('A') + 1)
    col += ord(cadena[-1]) - ord('A') + 1
    return col


def get_square_coordinates(sht_range_str='A35:JK288'):
    rc_init, rc_end = sht_range_str.split(':')
    col_init, row_init = extract_coordinates(rc_init)
    col_end, row_end = extract_coordinates(rc_end)
    return (row_init, column(col_init), row_end, column(col_end))


def get_range(row_init, row_end, col_init, col_end=None):
    if col_end is None:
        col = col_init
        range = '{}{}:{}{}'.format(col, row_init, col, row_end)
    else:
        range = '{}{}:{}{}'.format(col_init, row_init, col_end, row_end)

    return range

if __name__ == '__main__':
    if len(sys.argv) > 1:
        rng = sys.argv[1]
        print(get_square_coordinates(rng))
