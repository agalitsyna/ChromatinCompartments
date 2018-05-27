"""
These functions are borrowed from https://github.com/agalitsyna/pairsamtools/blob/ac0b717d243261eb9092a47ed3e9e31832c5f10f/examples_single_cell/WD/basic_utils.py
"""

import numpy as np
import pandas as pd

import glob
import cooler

import logging
logging.basicConfig(level=logging.INFO)

import time
from datetime import timedelta

import subprocess
import os

def cooler2hic(cool, outfile_hic,
               genome = 'dm3',
               resolutions = [10000,20000,100000],
               remove_intermediary_files = False,
               juicer_path = './juicer_tools.1.8.9_jcuda.0.8.jar', java_path='java'):
    """
    Converts .cool to Lieberman's .hic file. 

    :param cool: input .cool file
    :param outfile_hic: output .hic file
    :param genome: genome annotation name (one of hg18, hg19, hg38, dMel, mm9, mm10, anasPlat1, bTaurus3, canFam3,
        equCab2, galGal4, Pf3D7, sacCer3, sCerS288c, susScr3, or TAIR10) or a tab-delimited file with chromosomes sizes, default 'dm3'
    :param resolutions: list of resolutions that should be present in .hic file, default [10000,20000,100000]
    :param remove_intermediary_files: whether to remove intermediary .txt files, default False
    :param juicer_path: path to juicer .jar file, default './juicer_tools.1.8.9_jcuda.0.8.jar'
    :return: None
    """
    
    outfile_txt = outfile_hic + '.txt'
    outfile_tmp = outfile_hic + '.tmp'
    
    c = cooler.Cooler(cool)
    chromosomes = c.chromnames

    with open(outfile_tmp, 'w'):
        pass

    for chrom in chromosomes:
        cooler2txt_chr(cool, outfile_tmp,
                       fmt='sparse_coords',
                       chromosome=chrom,
                       writing_mode='a',
                       separator='\t')

    command1 = "awk '{{print 0, $1, $2, 0, 0, $4, $5, 1, $7}}' {} > {}".format(outfile_tmp, outfile_txt)
    command2 = "gzip -f {}".format(outfile_txt)
    command3 = "{} -Xmx2g -jar {} pre -r {} {}.gz {} {}".format(java_path, juicer_path, ','.join(list(map(str, resolutions))), outfile_txt, outfile_hic, genome)

    run_command(command1)
    run_command(command2)
    run_command(command3)
    
    if remove_intermediary_files:
        os.remove(outfile_txt+'.gz')
        os.remove(outfile_tmp)
        
def call_and_check_errors(command):
    
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            shell=True, executable='/bin/bash')
    (stdout, stderr) = proc.communicate()
    logging.info("Check stdout: {}".format(stdout))
    if stderr:
        logging.info("Stderr is not empty. Might be an error in call_and_check_errors for the command: {}".format(command))
        logging.info("Check stderr: {}".format(stderr))
        return stderr   # Error, very bad!
    else:
        return 0        # No error, great!

def run_command(command, force=False):

    logging.info(command)

    possible_outfile = command.split('>')

    if len(possible_outfile)>1:
        possible_outfile = possible_outfile[-1]
        if os.path.isfile(possible_outfile):
            if force:
                logging.info("Outfile {} exists. It will be overwritten!".format(possible_outfile))
            else:
                raise Exception("Outfile {} exists. Please, delete it, or use force=True to overwrite it.".format(possible_outfile))

    cmd_bgn_time = time.time()
    is_err = call_and_check_errors(command)
    cmd_end_time = time.time()
    
    return is_err