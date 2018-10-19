def extract_letters(col_row_notation='JK288'):
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


def obtains_rows(sht_range_str='A35:JK288'):
    rc_init, rc_end = sht_range_str.split(':')
    col_init, row_init = extract_letters(rc_init)
    col_end, row_end = extract_letters(rc_end)
    return (row_init, column(col_init), row_end, column(col_end))


class DataSheet():
    def __init__(self, spreadsheet, wk):
        self.data_sheet = wk
        self.parent = spreadsheet


class SearchInColumns():
    def __init__(self):
        self.column = 1
        self.current_row = 1


if __name__ == '__main__':
    print(obtains_rows())
