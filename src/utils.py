import GEOparse
import pandas as pd

gse_dict = {
    'Rao': 'GSE63525', 
    'Bonev': 'GSE96107',
    'Ulyanov': 'GSE69013',
    'Zuin': 'GSE44267',
    'Dekker_A549': 'GSE105600',
    'Dekker_HEpG2':'GSE105381',
    'Barutcu':'GSE66733',
    'Stadhouders':'GSE96611'
}

fastq_dump_options={'split-files': None,
    'read-filter': 'pass',
    'dumpbase': None,
    'gzip': None}

def parse_metadata(gsm, mode='Ulyanov'):
    meta = gsm.metadata
    meta_parsed = {}

    if mode == 'Rao':
        meta_parsed['author'] = meta['contact_name'][0]
        meta_parsed['paper'] = "Rao 2014"
        meta_parsed['data'] = meta['submission_date'][0]
        meta_parsed['species'] = meta['organism_ch1'][0]
        meta_parsed['source'] = meta['source_name_ch1'][0]
        meta_parsed['cell type'] = meta['characteristics_ch1'][0].split(':')[1].strip()
        meta_parsed['stage'] = 'NA'
        meta_parsed['treatment'] = 'NA'
        meta_parsed['protocol short'] = meta['characteristics_ch1'][1].split(':')[1].strip()
        meta_parsed['protocol'] = ' '.join(meta['extract_protocol_ch1']).replace('\t', ' ')
        meta_parsed['processing'] = ' '.join(meta['data_processing']).replace('\t', ' ')
        meta_parsed['series'] = meta['geo_accession'][0]
        meta_parsed['rep'] = 'NA'
        
    elif mode == 'Stadhouders':
        meta_parsed = {}
        #meta = gsms[gsms.keys()[i]].metadata
        meta_parsed['author'] = meta['contact_name'][0]
        meta_parsed['paper'] = "Stadhouders 2018"
        meta_parsed['data'] = meta['submission_date'][0]
        meta_parsed['species'] = meta['organism_ch1'][0]
        meta_parsed['source'] = meta['source_name_ch1'][0]
        tp = meta['characteristics_ch1'][0].split()
        if 'bone' in tp:
            tp = 'bonemarrow'
        else:
            tp = 'embryo'
        meta_parsed['cell type'] = "{}_{}".format(tp, meta['title'][0].split('_')[0])
        meta_parsed['stage'] = meta['title'][0].split('_')[0]
        #meta_parsed['treatment'] = ' '.join(meta['treatment_protocol_ch1']).replace('\t', ' ')
        meta_parsed['treatment'] = 'NA'
        meta_parsed['protocol short'] = meta['library_strategy'][0]
        meta_parsed['protocol'] = ' '.join(meta['extract_protocol_ch1']).replace('\t', ' ')
        meta_parsed['processing'] = ' '.join(meta['data_processing']).replace('\t', ' ')
        meta_parsed['series'] = meta['geo_accession'][0]
        meta_parsed['rep'] = meta['title'][0][-1]
        
    elif mode == 'Bonev':
        meta_parsed['author'] = meta['contact_name'][0]
        meta_parsed['paper'] = "Bonev 2017"
        meta_parsed['data'] = meta['submission_date'][0]
        meta_parsed['species'] = meta['organism_ch1'][0]
        meta_parsed['source'] = meta['source_name_ch1'][0]
        meta_parsed['cell type'] = meta['characteristics_ch1'][0].split(':')[1].strip()
        meta_parsed['stage'] = 'NA'
        meta_parsed['treatment'] = 'No treatment'
        meta_parsed['protocol short'] = meta['title'][0]
        meta_parsed['protocol'] = ' '.join(meta['extract_protocol_ch1']).replace('\t', ' ')
        meta_parsed['processing'] = ' '.join(meta['data_processing']).replace('\t', ' ')
        meta_parsed['series'] = meta['geo_accession'][0]
        meta_parsed['rep'] = 'NA'

    elif mode == 'Ulyanov':
        meta_parsed['author'] = meta['contact_name'][0]
        meta_parsed['paper'] = "Ulyanov 2015"
        meta_parsed['data'] = meta['submission_date'][0]
        meta_parsed['species'] = meta['organism_ch1'][0]
        meta_parsed['source'] = meta['source_name_ch1'][0]
        meta_parsed['cell type'] = meta['characteristics_ch1'][0].split(':')[1].strip()
        meta_parsed['stage'] = 'NA'
        meta_parsed['treatment'] = 'NA'
        meta_parsed['protocol short'] = meta['title'][0].split('_')[1]
        meta_parsed['protocol'] = ' '.join(meta['extract_protocol_ch1']).replace('\t', ' ')
        meta_parsed['processing'] = ' '.join(meta['data_processing']).replace('\t', ' ')
        meta_parsed['series'] = meta['geo_accession'][0]
        try:
            meta_parsed['rep'] = meta['title'][0].split('_')[2]
        except Exception as e:
            meta_parsed['rep'] = 'NA'

    elif mode == 'Barutcu':
        meta_parsed['author'] = meta['contact_name'][0]
        meta_parsed['paper'] = "Barutcu 2015"
        meta_parsed['data'] = meta['submission_date'][0]
        meta_parsed['species'] = meta['organism_ch1'][0]
        meta_parsed['source'] = meta['source_name_ch1'][0]
        meta_parsed['cell type'] = meta['characteristics_ch1'][0].split(':')[1].strip()
        meta_parsed['stage'] = 'NA'
        meta_parsed['treatment'] = 'NA'
        meta_parsed['protocol short'] = meta['title'][0].split()[1]
        meta_parsed['protocol'] = ' '.join(meta['extract_protocol_ch1']).replace('\t', ' ')
        meta_parsed['processing'] = ' '.join(meta['data_processing']).replace('\t', ' ')
        meta_parsed['series'] = meta['geo_accession'][0]
        try:
            meta_parsed['rep'] = meta['title'][0].split('_')[2]
        except Exception as e:
            meta_parsed['rep'] = 'NA'
            
    elif 'Dekker' in mode:
        meta_parsed['author'] = meta['contact_name'][0]
        meta_parsed['paper'] = "NA"
        meta_parsed['data'] = meta['submission_date'][0]
        meta_parsed['species'] = meta['organism_ch1'][0]
        meta_parsed['source'] = meta['source_name_ch1'][0]
        meta_parsed['cell type'] = meta['characteristics_ch1'][0].split(':')[1].strip()
        meta_parsed['stage'] = 'NA'
        meta_parsed['treatment'] = 'NA'
        
        meta_small = {y.split(':')[0]:y.split(':')[1].strip() for y in meta['description'][2:]}
        meta_parsed['protocol short'] = meta_small['assay title']
        meta_parsed['protocol'] = ' '.join(meta['extract_protocol_ch1']).replace('\t', ' ')
        meta_parsed['processing'] = ' '.join(meta['data_processing']).replace('\t', ' ')
        meta_parsed['series'] = meta['geo_accession'][0]
        meta_parsed['rep'] = meta_small['biological replicate number']

    elif mode == 'Zuin':
        meta_parsed['author']         = meta['contact_name'][0]
        meta_parsed['paper']          = "Zuin 2013"
        meta_parsed['data']           = meta['submission_date'][0]
        meta_parsed['species']        = meta['organism_ch1'][0]
        meta_parsed['source']         = meta['source_name_ch1'][0]
        meta_parsed['stage']          = 'NA'
        meta_parsed['protocol short'] = meta['title'][0].split(',')[0].strip()
        meta_parsed['protocol']       = ' '.join(meta['extract_protocol_ch1']).replace('\t', ' ')
        meta_parsed['processing']     = ' '.join(meta['data_processing']).replace('\t', ' ')
        meta_parsed['series']         = meta['geo_accession'][0]
        tmp = meta['title'][0].split(',')
        if len(tmp)==4:
            meta_parsed['treatment']      = tmp[2].strip()
            meta_parsed['cell type']      = tmp[1].strip()
            meta_parsed['rep']            = '1' if 'one' in tmp[3].strip() else '2' if 'two' in tmp[3].strip() else '?'
        else:
            meta_parsed['cell type']      = tmp[1].strip().split()[0]
            meta_parsed['treatment']      = ' '.join(tmp[1].strip().split()[1:])
            meta_parsed['rep']            = '1' if 'one' in tmp[2].strip() else '2' if 'two' in tmp[2].strip() else '?'
            
    meta_parsed['title'] = meta['title'][0]
    return meta_parsed
    
def download_regular(name, filterby=None, metadata_path="./", destdir="./TMP_SOFT", nthreads=20):

    geo_id = gse_dict[name]

    gse = GEOparse.get_GEO(geo=geo_id, destdir=destdir) 
    gsms = gse.gsms
    
    if filterby is None:
        downloaded_paths = gse.download_SRA('ljosudottir@gmail.com', filetype='fastq', fastq_dump_options=fastq_dump_options, nproc=nthreads, silent=True)
    else:
        downloaded_paths = gse.download_SRA('ljosudottir@gmail.com', filetype='fastq', filterby=filterby, fastq_dump_options=fastq_dump_options, nproc=nthreads, silent=True) # fix a bug with multiple replicates!
    
    metadata_collected_dict = {x: parse_metadata(gsms[x], mode=name) for x in downloaded_paths.keys()}

    metadata_collected_list = []
    for k in metadata_collected_dict:
        for i in range(len(downloaded_paths[k])//2):
            d = metadata_collected_dict[k]
            d['path fastq R1'] = downloaded_paths[k][2*i]
            d['path fastq R2'] = downloaded_paths[k][2*i+1]
            d['gse'] = geo_id
            metadata_collected_list.append(dict(d))

    df1 = pd.DataFrame(metadata_collected_list)
    
    df1 = pd.concat([g.drop('index', axis=1).reset_index(drop=True) for i, g in df1.reset_index().groupby("index")]).reset_index()
    df1.loc[:, 'technical_rep'] = df1.loc[:, 'index']+1
    df1 = df1.drop('index', axis=1)
    df1 = df1.applymap(lambda x: str(x).replace(' ', '-'))

    df1.loc[:, "running_mode"] = name
    df1.to_csv(os.path.join(metadata_path,'{}_metadata.tsv'.format(geo_id)), sep='\t')
    df1 = df1.drop(['processing', 'protocol'], axis=1)
    df1.to_csv(os.path.join(metadata_path,'{}_metadata_short.tsv'.format(geo_id)), sep='\t')
