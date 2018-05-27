# ChromatinCompartments

This is a small project to call chromatin compartments in a unified way from any Hi-C dataset. Operating system: 

It combines multiple tools for Hi-C data processing, including:

- [cooltools](https://github.com/mirnylab/cooltools/tree/master/cooltools)
- [juicer tools](https://github.com/theaidenlab/juicer/wiki/Juicer-Tools-Quick-Start)
- [distiller](https://github.com/mirnylab/distiller-nf)

and multiple sources of Hi-C datasets:
- [GEO](https://www.ncbi.nlm.nih.gov/geo/)
- [AidenLab datasets](https://aidenlab.org/data.html)

Other requirements: 
- [GEOparse parallel version](https://github.com/agalitsyna/GEOparse) for raw data download and parser
- [cooler](https://github.com/mirnylab/cooler) Python package
- basic anaconda scientific packages (pandas, numpy, scipy, matplotlib, seaborn) 
- java compatible with juicer tools version
- bwa

### TODO

1. Add thorough description of processed datasets.

2. Multi-species examples. 

3. Description of compartments calling details by different tools.

4. Distiller vs juicer processing protocols and references to the papers.

5. References section. 

### Usage
1. Download GEO entries.

```bash
python 01_download_GEO.py
```

This script downloads GEO SRA files with Hi-C fastq paired-end sequencing and produces unified metadata with information about replicates, treatment, cell types, species, publication and protocol details. 

Currently implemented downloads: 
- Rao 2014 (GSE63525, mouse and human Hi-C)
- Bonev (GSE96107, human Hi-C)
- Ulyanov 2015 (GSE69013, Drosophila Hi-C)
- Zuin (GSE44267)
- Dekker_A549 (GSE105600)
- Dekker_HEpG2 (GSE105381)
- Barutcu (GSE66733)
- Stadhouders (GSE96611)

SRA/FASTQ files will be downloaded to ../data/sra/ directory. Metadata will be stored to ../data/metadata/ directory. By default, 20 threads (processing cores) are used. 

2. Setup .yml file for distiller.

```bash
bash 02_setup_from_geo.sh
```

This script parses metadata from ../data/metadata and produces .yml file for distiller in ../data/distiller_yml/ directory.
The settings are nearly the same as in disiller examples, except for the size of fastq chunks. 

The script also sets up a folder with initial fastq and genome data. The folder with them will be located in the current working directory and called correspondingly to genome and id of dataset, e.g. test_hg19_Zuin. 

Please, note that before running this step genome file of interest should be downloaded as a single gzipped file, called by genome assembly name (e.g. hg19.fa.gz) and placed to ../data/genome/ folder.

Then you can run distiller in this folder with resulting .yml file (e.g. project_hg19_Zuin.yml).

3. Convert resulting .cool files to .hic and call compartments. 

```bash
jupyter notebook 
03_convert-call.ipynb
```

This step is implemented as jupyter notebook, although it might be divided to converted and calling parts and used as standalone scripts (both steps are time-consuming). 

Currently the only implemented way of compartments calling is per-chromosome call with juicer tools [Eigenvector](https://github.com/theaidenlab/juicer/wiki/Eigenvector), which might be not as advanced as whole-genome call including information about trans-interactions. 

Juicer tools are working with [AidenLab datasets](https://aidenlab.org/data.html) that are processed by juicer, not by distiller/cooler. For K562, HeLa, HMEC, NHEK, HUVEC, IMR90, GM12878 cell lines links for remote .hic files can be used for compartments calling by juicer tools. 

4. Visualize and compare first eigenvecotrs.

```bash
jupyter notebook 
04_correlation_analysis.ipynb
```

Analyse properties of comparments. note that cell types are not clustered by the processing method or lab (distiller or juicer).
