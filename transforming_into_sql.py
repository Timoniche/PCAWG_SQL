import os
import sys

import configparser
from sqlalchemy import create_engine
import pandas as pd

script_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')
resource = 'icgc'  # 'tcga'
csvspath = script_dir + fr'/csvs_{resource}'


def save_to_sql():
    config = configparser.ConfigParser()
    config.read(script_dir + r'/application.properties')
    user = config['DEFAULT']['pcawg.user']
    password = config['DEFAULT']['pcawg.password']
    engine = create_engine(f'postgresql://{user}:{password}@localhost:5432/pcawg')
    if not engine.has_table('sv_donor'):
        sv_donor = pd.read_csv(csvspath + '/sv_donor.csv')
        sv_donor.to_sql('sv_donor', engine, index=False)
    if not engine.has_table('sv_intra'):
        sv_intra = pd.read_csv(csvspath + '/simple_intra_sv.csv')
        sv_intra.to_sql('sv_intra', engine, index=False)
    if not engine.has_table('donor_tumour'):
        donor_tumour = pd.read_csv(csvspath + '/donor_tumour.csv')
        donor_tumour.to_sql('donor_tumour', engine, index=False)


def main():
    save_to_sql()


if __name__ == '__main__':
    main()
