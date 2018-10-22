

class DataSheet():
    def __init__(self, spreadsheet, wk):
        self.data_sheet = wk
        self.parent = spreadsheet


class SearchInColumns():
    def __init__(self, datasheet_in, range_in):
        square_dimensions = obtains_rows(range_in)
        self.start_row = square_dimensions[0]
        self.end_row = square_dimensions[2]
        self.values_to_look_in = [cell.value for cell in
                                  datasheet_in.range(range_in)]
        self.rows = None

    def look_for(self, datasheet, range_from, same_arrangement=True):
        self.values_to_look_from = [cell.value for cell in
                                    datasheet.range(range_from)]
        try:
            first_index = self.values_to_look_in.index(self.
                                                       values_to_look_from[0])
            first_row = first_index + self.start_row
            if same_arrangement:
                self.rows = [index + self.start_row
                             for index in range(len(self.values_to_look_from))]
        except ValueError:
            print("Error: No se encuentra el primer valor de la serie")
            raise ValueError

    def get_values(self, datasheet, range_from):
<<<<<<< HEAD
        pass

=======
        
>>>>>>> aee7289cfc7039443f47c266026a2d765b5b2240

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


if __name__ == '__main__':
    print(obtains_rows())
