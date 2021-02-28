import os
import sys
import glob
import pandas as pd

script_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')
datapath = script_dir + r'/data'
csvspath = script_dir + r'/csvs'


# filehashes_donorid.csv consists 'tumor_wgs_aliquot_id' column with comma-separated file hashes
def build_donors_csvs():
    donors_excel = pd.read_excel(datapath + r'/pcawg-data-releases.xlsx')
    donors_excel.to_csv(csvspath + r'/donors.csv', index=False)
    projection = ['tumor_wgs_aliquot_id', 'submitter_donor_id']
    donors_excel.to_csv(csvspath + r'/filehashes_donorid.csv', index=False, columns=projection)


def build_filehash_donorid_map():
    if not os.path.exists(csvspath + r'/filehashes_donorid.csv'):
        build_donors_csvs()
    filehashes_donorid_csv = pd.read_csv(csvspath + r'/filehashes_donorid.csv')
    filehash_donorid_map = {}
    for idx, row in filehashes_donorid_csv.iterrows():
        filehashes = row['tumor_wgs_aliquot_id'].split(sep=',')
        for filehash in filehashes:
            filehash_donorid_map[filehash] = row['submitter_donor_id']
    return filehash_donorid_map


def build_sv_with_donor_csv():
    filehash_donorid_map = build_filehash_donorid_map()
    os.chdir(datapath + r'/icgc/open')
    csvs = []
    for file in glob.glob('*.gz'):
        file_hash_prefix = file.split(sep='.')[0]
        donor_id = filehash_donorid_map.get(file_hash_prefix)
        cur_csv = pd.read_csv(file, sep='\t')
        cur_csv['donor_id'] = donor_id
        csvs.append(cur_csv)
    sv_donor_csv = pd.concat(csvs)
    sv_donor_csv.to_csv(csvspath + r'/sv_donor.csv', index=False)


def main():
    build_sv_with_donor_csv()


if __name__ == '__main__':
    main()