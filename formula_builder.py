import gspread
from utils import DataSheetSettings
from utils import ReaderDataSheet
from utils import get_matrix_form_range
from oauth2client.service_account import ServiceAccountCredentials


SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

KEY_FILE = 'transcriptional-model-key.json'
OUTPUT_TMP = '/tmp/formulas.txt'

def to_file(values_dict, path):
    import ipdb; ipdb.set_trace()
    with open(path, 'w') as file:
        for key, val in values_dict.items():
            file.write('{}:\n'.format(key))
            file.write('{}:\n'.format(val))




class Formula():
    def __init__(self, raw_formula):
        self.raw_formula = raw_formula.strip()

    def get_instance(self, row_values):
        instantiated_formula = self.raw_formula[:]
        for index, value in enumerate(row_values):
            instantiated_formula = instantiated_formula.replace('[{}]'.format(index),
                value)
        return instantiated_formula


def formula_TSCR_ini_TUxxx(reader):
    '''
    Transcription initiation of (rho independent)
    1 RNAP_xxx  + xx atp + 1 TUxxx_DNA_act + xx ctp + xx gtp + xx utp
    <=> 1 Rpox_mono_inact + xxx ppi +  transcr_ini_x_cplx

    Example:
    TU_187732
    RNAP_70 + TU_187732_DNA_act + 6 atp + 2 ctp + 5 gtp + 3 utp
    <=> RpoD_mono_inact + 15 ppi + transcr_ini_TU_187732_cplx

    TU_532800
    RNAP_70 + TU_532800_DNA_act + 6 atp + 2 ctp + 3 gtp + 3 utp
    <=> RpoD_mono_inact + 15 ppi + transcr_ini_TU_532800_cplx
    '''

    formula = Formula(reader.read_from('Templates', 'C21'))
    # values = reader.remove_empty_lines('Datos', 'A4:H282')
    values = reader.remove_empty_lines('Datos', 'A4:H282')

    results = {}
    for row in values:
        row_values = [cell.value for cell in row]
        results[row_values[0]] = formula.get_instance(row_values)

    to_file(results, OUTPUT_TMP)



def main():
    config = DataSheetSettings(KEY_FILE, SCOPE)
    reader = ReaderDataSheet('ematix_05_10', config)
    formula_TSCR_ini_TUxxx(reader)



if __name__ == '__main__':
    main()
