"""
Python script to download GEO entries with Hi-C fastq and create file with metadata.
Note that GEOparse version https://github.com/agalitsyna/GEOparse is required.
"""

from utils import *

filters_dict = {
    'Zuin'        : lambda x: 'Hi-C' in x.metadata['title'][0],
    'Stadhouders' : lambda x: 'Hi' in x.metadata['title'][0],
    'Dekker_HEpG2': None,
    'Dekker_A549' : None,
    'Barutcu'     : None,
    'Rao'         : lambda x: 'Hi-C' in x.metadata['characteristics_ch1'][1],
    'Ulyanov'     : lambda x: 'Hi-C' in x.metadata['title'][0],
    'Bonev'       : lambda x: 'Hi-C' in x.metadata['library_strategy'],
    'Stadhouders' : lambda x: 'Hi' in x.metadata['title'][0]
}

mode = 'Rao'
download_regular(mode, filterby=filters_dict[mode], destdir="../data/sra/", metadata_path="../data/metadata", nthreads=20)