import gspread
from utils import DataSheetSettings
from utils import ReaderDataSheet
from utils import get_matrix_form_range
from oauth2client.service_account import ServiceAccountCredentials


SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

KEY_FILE = 'transcriptional-model-key.json'

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
    formula = reader.read_from('Templates', 'C21')
    # values = reader.filtered_values('Datos', 'A4:H282', 'empty_rows')
    values = reader.filtered_values('Datos', 'A4:B9', 'empty_rows')
    # values_collection = base_datasheet.range(self.init_row, self.init_col,
    #                                self.end_row, self.end_col)
    #

    import ipdb; ipdb.set_trace()


def main():
    config = DataSheetSettings(KEY_FILE, SCOPE)
    reader = ReaderDataSheet('ematix_05_10', config)
    formula_TSCR_ini_TUxxx(reader)



if __name__ == '__main__':
    main()
