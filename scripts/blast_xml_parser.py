#This script will parse through an xml blast output file and extract all the genes above a certain bitscore and write them out in a new csv file

import Bio, sys, os, glob, csv, subprocess

'''
usage: blast_xml_parser.py input_xml, bit_score_cutoff
'''

out_filename_start = sys.argv[1].split('.')
out_filename = out_filename_start[0] + '.txt'
out_list = open(out_filename, 'w')
out_list.close()

out_filename_info = out_filename_start[0] + '_info.txt'
out_list_info = open(out_filename_info, 'w')
out_list_info.close()

out_filename_faa = out_filename_start[0] + '.faa'
out_list_faa = open(out_filename_faa, 'w')
out_list_faa.close()


bit_cutoff = int(sys.argv[2])

#Parse through the xml file printing those genes with a bitscore higher than the given cutoff
from Bio.Blast import NCBIXML
filename = sys.argv[1]
result=open(filename,"r")
records= NCBIXML.parse(result)
item=next(records)
for alignment in item.alignments:
	 for hsp in alignment.hsps:
		if hsp.bits > bit_cutoff:
				print('****Alignment****')
				sequence = 'sequence: ' + alignment.accession
				length = 'length: ' + str(alignment.length)
				bitscore = 'bitscore: ' + str(hsp.bits)
				score = 'score: ' + str(hsp.score)
				evalue = 'evalue: ' + str(hsp.expect)
				ident = 'identities: ' + str(hsp.identities)
				positive = 'positive: ' + str(hsp.positives)
				gaps = 'gaps: ' + str(hsp.gaps)
				print sequence
				print length
				print bitscore
				print score
				print evalue
				print ident
				print positive
				print gaps
				print(hsp.query[0:])
				print(hsp.match[0:])
				print(hsp.sbjct[0:])
				with open(out_filename, 'a') as gene_append:
					gene_append.write(alignment.accession)
					gene_append.write('\n')
				with open(out_filename_info, 'a') as gene_append_info:
					gene_append_info.write('****Alignment****')
					gene_append_info.write('\n')
					gene_append_info.write(sequence)
					gene_append_info.write('\n')
					gene_append_info.write(length)
					gene_append_info.write('\n')
					gene_append_info.write(bitscore)
					gene_append_info.write('\n')
					gene_append_info.write(score)
					gene_append_info.write('\n')
					gene_append_info.write(evalue)
					gene_append_info.write('\n')
					gene_append_info.write(ident)
					gene_append_info.write('\n')
					gene_append_info.write(positive)
					gene_append_info.write('\n')
					gene_append_info.write(gaps)
					gene_append_info.write('\n')
					gene_append_info.write(hsp.query[0:])
					gene_append_info.write('\n')
					gene_append_info.write(hsp.match[0:])
					gene_append_info.write('\n')
					gene_append_info.write(hsp.sbjct[0:])
					gene_append_info.write('\n')
				with open(out_filename_faa, 'a') as gene_append_faa:
					fasta_header = '> ' + alignment.accession
					gene_append_faa.write(fasta_header)
					gene_append_faa.write('\n')
					gene_append_faa.write(hsp.sbjct[0:])
					gene_append_faa.write('\n')
