#This script will take in genomes (fastas or fnas), create a local blast database and then
#blast against the the database with a given sequence and return all the genes (and by extension
#organisms) which match (or contain the gene).

#Should work on either nucleotide or protein sequences.

#Blast+ commands must be in the PATH variable/local bin and can be called by, for example, merely
#makeblastdb

import Bio, sys, os, glob, csv, subprocess

'''
usage: gene_searcher_with_blast.py input_directory, output_directory, input_seq
'''

#input_directory = directory containing fnas or faas for all organisms which you wish to search
#through for the given sequence
#output_directory = directory where you wish to put the constructed blast database and blast
#search file and conmbined fna file
#input_seq = fasta file containing the sequence for which you wish to blast the organisms against

from Bio.Blast.Applications import NcbiblastnCommandline
from Bio.Blast.Applications import NcbiblastpCommandline

def blast_db_maker(input_directory, output_directory):

	for root, dirs, files in os.walk(input_directory):
		file_list = [i for i in files if i.endswith('.fna')]
		print file_list
		empty = []
		if file_list == empty:
			file_list = [i for i in files if i.endswith('.faa')]
			print file_list

	if '.fna' in file_list[0]:
		output_fasta = output_directory + 'combined_fna.fna'
		args_str = 'makeblastdb -in ' + output_fasta + ' -out ' + output_directory + 'combined_blast_db_n' + ' -parse_seqids -dbtype nucl'
	if '.faa' in file_list[0]:
		output_fasta = output_directory + 'combined_faa.faa'
		args_str = 'makeblastdb -in ' + output_fasta + ' -out ' + output_directory + 'combined_blast_db_p' + ' -parse_seqids -dbtype prot'

	with open(output_fasta, 'w') as outfile:
		for fname in file_list:
			fname = input_directory + fname
			with open(fname) as infile:
				for line in infile:
					outfile.write(line)


	args = str.split(args_str)
	print args
	subprocess.call(args)
	return file_list



file_list = blast_db_maker(sys.argv[1], sys.argv[2])


def blast_run_nucleotide(output_directory, input_seq):
	blast_db_n = output_directory + 'combined_blast_db_n'
	search_name = str.split(input_seq,'.')
	out_name = search_name[0] + '.xml'
	blastn_cline = NcbiblastnCommandline(query=input_seq, db=blast_db_n, evalue=0.001, outfmt=5, out=out_name)
	blastn_cline
	print(blastn_cline)
	stdout, stderr = blastn_cline()

if '.fna' in file_list[0]:
	blast_run_nucleotide(sys.argv[2], sys.argv[3])

def blast_run_protein(output_directory, input_seq):
	blast_db_p = output_directory + 'combined_blast_db_p'
	search_name = str.split(input_seq,'.')
	out_name = search_name[0] + '.xml'
	blastp_cline = NcbiblastpCommandline(query=input_seq, db=blast_db_p, evalue=.001, outfmt=5, out=out_name)
	blastp_cline
	print(blastp_cline)
	stdout, stderr = blastp_cline()

if '.faa' in file_list[0]:
	blast_run_protein(sys.argv[2], sys.argv[3])




