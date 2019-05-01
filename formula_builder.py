import re
from utils import DataSheetSettings
from utils import ReaderDataSheet
from utils import get_square_coordinates
from utils import column

SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

KEY_FILE = 'transcriptional-model-key.json'
OUTPUT_TMP = '/tmp/formulas.txt'


def to_file(values_dict, path):
    with open(path, 'w') as file:
        for key, val in values_dict.items():
            file.write('{}:\n'.format(key))
            file.write('{}:\n'.format(val))


class Formula():
    def __init__(self, raw_formula):
        self.raw_formula = raw_formula.strip()

    def get_instance(self, row_values):
        instantiated_formula = self.raw_formula[:]
        search_iter = re.finditer(r'\[.*?([A-Z])\d+\]', instantiated_formula)
        for search in search_iter:
            if search:
                col = column(search.groups()[0])
            for value in row_values:
                if value.col == col:
                    instantiated_formula = instantiated_formula.replace(search.group(),
                                                                        value.value)
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


def formula_tscr_elo_TU_xxxx_ini_rho_dep(reader):
    formula_rho_dep = Formula(reader.read_from('Templates', 'C22'))
    formula_rho_indep = Formula(reader.read_from('Templates', 'C23'))

    values = reader.remove_empty_lines('Datos', 'A4:H282')
    conditions = reader.remove_empty_lines('Datos', 'P4:Q282')
    results = {}

    for index, row in enumerate(conditions):
        dep = row[0].value.strip()
        row_values = [cell for cell in values[index]]
        results[row_values[0]] = formula_rho_dep.get_instance(row_values) \
            if dep.upper() == 'OK' else formula_rho_indep.get_instance(row_values)

    to_file(results, '/home/macastro/rho_dep_indep_output.txt')


def formula_DNA_binding_activator(reader):
    """
    [A4]_DNA_neu --> [A4]_DNA_act
    """
    formula = Formula(reader.read_from('Templates', 'C29'))
    values = reader.remove_empty_lines('Datos', 'A4:A282')
    results = {}
    for row in values:
        results[row[0]] = formula.get_instance(row)
    to_file(results, OUTPUT_TMP)


def formula_xxx_mRNA_CONV(reader):
    """
    1 [Datos_2!C5]_v1_mRNA --> 1 [Datos_2!C5]_mRNA_1
    """
    formula = Formula(reader.read_from('Templates', 'C37'))
    values = reader.remove_empty_lines('Datos_2', 'C5:C287')
    results = {}
    for row in values:
        results[row[0]] = formula.get_instance(row)

    to_file(results, OUTPUT_TMP)




def main():
    config = DataSheetSettings(KEY_FILE, SCOPE)
    reader = ReaderDataSheet('ematix_05_10', config)
    # formula_tscr_elo_TU_xxxx_ini_rho_dep(reader)
    # formula_DNA_binding_activator(reader)
    formula_xxx_mRNA_CONV(reader)

if __name__ == '__main__':
    main()
