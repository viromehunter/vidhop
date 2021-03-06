"""
MPT command line.
"""

import click
from .vidhop import path_to_fastaFiles, start_analyses
import sys
# import os


@click.command()
@click.option('--input', '-i', required=True, help='either raw sequences or path to fasta file or directory with multiple files.')
@click.option('--virus', '-v', required=True, help='select virus species (influ, rabies, rota)')
@click.option('--outpath', '-o', help='path where to save the output')
@click.option('--n_hosts', '-n', default=int(0), help='show only -n most likely hosts')
@click.option('--thresh', '-t', default=float(0), help='show only hosts with higher likeliness then --thresh')
@click.option('--auto_filter', '-f', is_flag=True, help='automatically filters output to present most relevant host')
@click.version_option(version=0.2, prog_name="VIrus Deep learning HOst Predictor")

def cli(input, virus, outpath, n_hosts, thresh, auto_filter):
    '''
    Example:

    \b
    $ vidhop -i /home/user/fasta/influenza.fna -v influ
    \b
    present only hosts which reach a threshold of 0.2
    $ vidhop -i /home/user/fasta/influenza.fna -v influ -t 0.2
    \b
    if you want the output in a file
    $ vidhop -i /home/user/fasta/influenza.fna -v influ -o /home/user/vidhop_result.txt
    \b
    use multiple fasta-files in directory
    $ vidhop -i /home/user/fasta/ -v rabies
    \b
    use multiple fasta-files in directory and only present top 3 host predictions per sequence
    $ vidhop -i /home/user/fasta/ -v rabies -n_hosts
    '''

    assert virus in ["rota","influ","rabies"], "not correct --virus parameter, use either rota, influ, or rabies"
    assert thresh >= 0 and thresh <=1, "error parameter --thresh: only thresholds between 0 and 1 allowed"
    assert n_hosts >= 0, "error parameter --n_hosts: only positive number of hosts allowed"

    if outpath:
        sys.stdout = open(outpath, 'w')
    header_dict = path_to_fastaFiles(input)
    for key, value in header_dict.items():
        start_analyses(virus=virus,top_n_host=n_hosts,threshold=thresh,X_test_old=value,header=key, auto_filter=auto_filter)

cli()