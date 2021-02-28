import os
import sys

import configparser
from sqlalchemy import create_engine
import pandas as pd

script_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')
datapath = script_dir + r'/data'
csvspath = script_dir + r'/csvs'


def save_to_sql():
    config = configparser.ConfigParser()
    config.read(script_dir + r'/application.properties')
    user = config['DEFAULT']['pcawg.user']
    password = config['DEFAULT']['pcawg.password']
    engine = create_engine(f'postgresql://{user}:{password}@localhost:5432/pcawg')
    if not engine.has_table('sv_donor'):
        sv_donor = pd.read_csv(csvspath + '/sv_donor.csv')
        sv_donor.to_sql('sv_donor', engine, index=False)


def main():
    save_to_sql()


if __name__ == '__main__':
    main()
