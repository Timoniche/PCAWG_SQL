import errno
import os
import sys
import glob
import time

import pandas as pd

script_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')
resource = 'icgc'  # 'tcga'
datapath = script_dir + r'/data'
bedpe_ = datapath + fr'/{resource}/open'
csvspath_ = script_dir + fr'/csvs_{resource}'


# filehashes_donorid.csv consists 'tumor_wgs_aliquot_id' column with comma-separated file hashes
def build_donors_csvs(csvspath):
    donors_excel = pd.read_excel(datapath + r'/pcawg-data-releases.xlsx')
    donors_excel.to_csv(csvspath + r'/donors.csv', index=False)
    projection = ['tumor_wgs_aliquot_id', 'submitter_donor_id']
    donors_excel.to_csv(csvspath + r'/filehashes_donorid.csv', index=False, columns=projection)


def build_filehash_donorid_map(csvspath):
    if not os.path.exists(csvspath + r'/filehashes_donorid.csv'):
        build_donors_csvs(csvspath)
    filehashes_donorid_csv = pd.read_csv(csvspath + r'/filehashes_donorid.csv')
    filehash_donorid_map = {}
    for idx, row in filehashes_donorid_csv.iterrows():
        filehashes = row['tumor_wgs_aliquot_id'].split(sep=',')
        for filehash in filehashes:
            filehash_donorid_map[filehash] = row['submitter_donor_id']
    return filehash_donorid_map


def build_sv_with_donor_csv(csvspath, bedpepath):
    filehash_donorid_map = build_filehash_donorid_map(csvspath)
    os.chdir(bedpepath)
    csvs = []
    for file in glob.glob('*.gz'):
        file_hash_prefix = file.split(sep='.')[0]
        donor_id = filehash_donorid_map.get(file_hash_prefix)
        cur_csv = pd.read_csv(file, sep='\t')
        cur_csv['donor_id'] = donor_id
        csvs.append(cur_csv)
    sv_donor_csv = pd.concat(csvs)
    sv_donor_csv.to_csv(csvspath + r'/sv_donor.csv', index=False)


def build_simplified_sv(csvspath):
    # from .bedpe doc (start, end]
    projection = ['chrom1', 'end1', 'chrom2', 'end2', 'donor_id']
    simplified_csv = pd.read_csv(csvspath + '/sv_donor.csv', usecols=projection)
    simplified_csv.rename(
        columns={'end1': 'bp1', 'end2': 'bp2'}, inplace=True
    )
    simplified_csv.to_csv(csvspath + r'/simple_sv.csv', index=False)
    intra_sv = simplified_csv[simplified_csv['chrom1'] == simplified_csv['chrom2']]
    simple_intra_sv = intra_sv[['chrom1', 'bp1', 'bp2', 'donor_id']].rename(
        columns={'chrom1': 'chr'}
    )
    simple_intra_sv.to_csv(csvspath + r'/simple_intra_sv.csv', index=False)


def build_tumour_type_csv(csvspath):
    donor_tumour = pd.read_excel(datapath + r'/pcawg_specimen_histology_August2016_v9.xlsx')
    donor_tumour.to_csv(csvspath + r'/donor_tumour.csv', index=False)


def create_dir(dirpath):
    if not os.path.exists(os.path.dirname(dirpath)):
        try:
            os.makedirs(os.path.dirname(dirpath))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def main():
    t1 = time.time()
    create_dir(csvspath_ + '/')
    build_tumour_type_csv(csvspath_)
    build_sv_with_donor_csv(csvspath_, bedpe_)
    build_simplified_sv(csvspath_)
    t2 = time.time()
    print(f'took {t2 - t1} sec')


if __name__ == '__main__':
    main()
