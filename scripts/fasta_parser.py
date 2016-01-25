#This script will search through a fasta file and construct a new fasta file composed of only those genes that correspond
#to an ortholog present in all the organisms in a set. The new fasta files will contain the orthologous genes in the same 
#order for all organsims.

#Credit to http://www.dalkescientific.com/writings/NBN/parsing.html for help constructing the code

import Bio, sys, os, glob, csv

'''
usage: fasta_parser.py fasta_directory, shared_orthologs
'''
#fasta_directory =  containing the fasta files you wish to parse
#for example: bacteroidetes_annotated_fasta/
#shared_orthologs = output of unique_ortho_finder.R, a matrix containing a list of orthologs (without any paralogs) shared between all the organisms and the list of the genes within each organism
#for example: bacteroidetes_results/all_organism_orthologs.csv

print 'fasta_directory = ' + sys.argv[1]

def fasta_list_maker(directory):
	#create a list of all the fasta files in the given directory
	fastas = []
	for root, dirs, files in os.walk(directory):
	    for file in files:
	    	if file.endswith('.faa' or '.fasta'):
	    		fastas.append(file)
	return fastas

fasta_list = fasta_list_maker(sys.argv[1])

print 'List of fastas:'
print fasta_list

def ortho_list_reader(orthologs):
	#input the list of orthologs and corresponding genes
	with open(orthologs, 'rb') as csvfile:
		ortho_list = csv.reader(csvfile)
		for row in ortho_list:
			ortho_list_read ='\n'.join(row)
			print '\n'.join(row)
	return ortho_list_read

ortho_list = ortho_list_reader(sys.argv[2])

print ortho_list





