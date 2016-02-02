#This script will search through a directory of .fna files and using a list of common orthologs,
#create new .fna files for each gene containing the the gene for each organism.

import Bio, sys, os, glob, csv, re

'''
usage: fna_parser_gene_constructer.py fna_directory, shared_orthologs, output_directory
'''
#fna_directory = directory containing the fasta files you wish to parse
#for example: bacteroidetes_annotated_fnas/
#shared_orthologs = output of unique_ortho_finder.R, a matrix containing a list of orthologs (without any paralogs) shared between all the organisms and the list of the genes within each organism
#for example: bacteroidetes_results/all_organism_orthologs.csv
#output_directory = directory to save the new fnas to
#for example: bacteroidetes_gene_fnas

print 'fna_directory = ' + sys.argv[1]

def fna_list_maker(directory):
	#create a list of all the fasta files in the given directory
	fnas = []
	for root, dirs, files in os.walk(directory):
	    for file in files:
	    	if file.endswith('.fna'):
	    		fnas.append(file)
	return fnas

fna_list = fna_list_maker(sys.argv[1])

print 'List of fnas:'
print fna_list

def ortho_list_reader(orthologs):
	#input the list of orthologs as a csv and output a list to be used within the python code
	with open(orthologs, 'rb') as csvfile:
		ortho_list = csv.reader(csvfile)
		ortho_list_read = list(ortho_list)
		#for row in ortho_list:
		#	ortho_list_read = ortho_list_read.join(row)
		#	print '\n'.join(row)
	return ortho_list_read

ortho_list = ortho_list_reader(sys.argv[2])

print ortho_list

def fna_file_maker(ortho_list, output_directory):
	#create empty fna files for each orthologous gene
	for ortholog_gene in ortho_list:
			ortho = ortholog_gene[0]
			if ortho != '':
				fna_save_file = output_directory + ortho[:-1] + '.fna'
				print fna_save_file
				gene_fna_file = open(fna_save_file, 'w')
				gene_fna_file.close()


fna_file_maker(ortho_list, sys.argv[3])

def fna_contstucter(fna_directory, fna_list, ortho_list, output_directory):
	#contstruct the fna file for each ortholog by adding the nucleotide sequences for each organism's orthologous gene. Genes are always added in the same order
	organism_number = len(fna_list)
	for fna_file in fna_list:
		from Bio import SeqIO
		filename = ()
		filename = fna_directory + fna_file
		print filename
		record_dict = SeqIO.to_dict(SeqIO.parse(filename, 'fasta'))
		print len(record_dict)
		for ortholog_gene in ortho_list:
			ortho = ortholog_gene[1:organism_number+1]
			print ortho
			for organism in ortho:
				print organism
				match_file = re.search('^.*\.\d*\.', fna_file)
				match_organism = re.search('\d.*\.\d*\.', organism)
				if match_organism:
					if match_organism.group(0) == match_file.group(0):
						print match_file.group(0)
						print match_organism.group(0)
						gene_id = '>' + str(record_dict[organism].id) + '\n'
						sequence = str(record_dict[organism].seq) + '\n'
						print gene_id
						print sequence
						ortho_id = ortholog_gene[0]
						fna_save_file = output_directory + ortho_id[:-1] + '.fna'
						print fna_save_file
						with open(fna_save_file, 'a') as gene_append:
							gene_append.write(gene_id)
							gene_append.write(sequence)

fna_contstucter(sys.argv[1], fna_list, ortho_list, sys.argv[3])



