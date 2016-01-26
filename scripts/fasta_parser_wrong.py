#This script will search through a fasta file and construct a new fasta file composed of only those genes that correspond
#to an ortholog present in all the organisms in a set. The new fasta files will contain the orthologous genes in the same 
#order for all organsims.

import Bio, sys, os, glob, csv, re

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
		ortho_list_read = list(ortho_list)
		#for row in ortho_list:
		#	ortho_list_read = ortho_list_read.join(row)
		#	print '\n'.join(row)
	return ortho_list_read

ortho_list = ortho_list_reader(sys.argv[2])

print ortho_list

def fasta_contstucter(fasta_directory, fasta_list, ortho_list):
	organism_number = len(fasta_list)
	for fasta_file in fasta_list:
		from Bio import SeqIO
		selected_genes = []
		filename = ()
		filename = fasta_directory + fasta_file
		print filename
		record_dict = SeqIO.to_dict(SeqIO.parse(filename, 'fasta'))
		print len(record_dict)
		for ortholog_gene in ortho_list:
			ortho = ortholog_gene[1:organism_number+1]
			print ortho
			for organism in ortho:
				print organism
				match_file = re.search('^.*\.', fasta_file)
				print match_file.group(0)
				match_organism = re.search('\d.*\.\d*\.', organism)
				if match_organism:
					print match_organism.group(0)
					if match_organism.group(0) == match_file.group(0):
						print record_dict[organism].seq
						sequence = str(record_dict[organism].seq)
						selected_genes.append(sequence)
						#print selected_genes
		#print selected_genes

		amino_acids = ''.join(selected_genes)
		#print amino_acids
		save_file = sys.argv[1] + match_file.group(0) + 'txt'
		text_file = open(save_file, 'w')
		text_file.write(amino_acids)
		text_file.close()





fasta_contstucter(sys.argv[1], fasta_list, ortho_list)



