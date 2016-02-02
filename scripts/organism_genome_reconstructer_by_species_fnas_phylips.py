#This script will search through a directory that contains .fna.muscle.BMGE files for a species 
#and construct a fna for the entire species containing a genome for each organism. The genome 
#will be only the previously selected orthologs that have been aligned and trimmed and will be
#made in the same order for all organisms. The .fna will be constructed so the header is the
#organism identifier followed by the reconstructed orthologous genome in the Phylip format.

import Bio, sys, os, glob, csv, re

'''
usage: organism_genome_reconstructer_by_species_fnas_phylips.py input_directory, output_directory
'''
#input_directory =  containing files you wish to parse
#for example: bacteroidetes_gene_fnas/
#output_directory = directory to save the new fnas to
#for example: bacteroidetes_all_fna

print 'input_directory = ' + sys.argv[1]

def BMGE_and_organism_list_maker(directory):
	#create a list of all the .BMGE files in the given directory, giving a list of every gene
	#that must be read and concatanated to create the orthologous genomes
#	BMGEs = []
	for root, dirs, files in os.walk(directory):
#	    for file in files:
#	    	if file.endswith('.BMGE'):
#	    		ortho_gene_id = re.search('^\w*', file)
#	    		BMGEs.append(ortho_gene_id.group(0))
	    BMGE_list = [i for i in files if i.endswith('.BMGE')] #should be faster than above method
	    												#removing file type isn't needed
	    from Bio import SeqIO
	    single_gene = directory + BMGE_list[0]
	    gene_dict = SeqIO.to_dict(SeqIO.parse(single_gene, 'fasta'))
	    organism_list = []
    	for key in gene_dict.keys():
    		organism_id = re.search('\d*\.\d*(?=\.)', key)
    		organism_list.append(organism_id.group(0))

	return {'organism_list': organism_list, 'BMGE_list': BMGE_list}

BMGE_organism_list = BMGE_and_organism_list_maker(sys.argv[1])

BMGE_list = BMGE_organism_list['BMGE_list']
organism_list = BMGE_organism_list['organism_list']

print 'List of BMGEs:'
print BMGE_list
print 'List of organisms:'
print organism_list


def fna_all_file_maker(output_directory):
	fna_save_file = output_directory + 'all_organisms.fna'
	phylp_save_file = output_directory + 'all_organisms.phylp'
	print fna_save_file
	gene_fna_file = open(fna_save_file, 'w')
	gene_fna_file.close()
	phylp_file = open(phylp_save_file, 'w')
	phylp_file.close()


#fna_all_file_maker(sys.argv[2])

def all_fna_contstucter(BMGE_list, organism_list, input_directory, output_directory):
	#create phylip style files to be used in PhyML in the construction of phylogenetic trees
	#Techinically the phylip sequence id is longer than 10 characters which is against the phylip
	#format but PhyML can read ids up to 100 characters
	organism_number = len(organism_list)
	fna_save_file = output_directory + 'all_organisms.fna'
	phylp_save_file = output_directory + 'all_organisms.phylip'
	print fna_save_file
	print phylp_save_file
	gene_fna_file = open(fna_save_file, 'w')
	gene_fna_file.close()
	phylp_file = open(phylp_save_file, 'w')
	phylp_file.close()
	for orga in organism_list:
		from Bio import SeqIO
		orga_id = '>' + orga + '\n'
		phylp_id = orga + ' '
		selected_seqs = []
		phylp_seqs = []
		print orga_id
		for filename in BMGE_list:
			filename = input_directory + filename
			print filename
			record_dict = SeqIO.to_dict(SeqIO.parse(filename, 'fasta'))
			for key in record_dict.keys():
				gene_orga_id = re.search('\d*\.\d*(?=\.)', key)
				if gene_orga_id.group(0) == orga:
					sequence = str(record_dict[key].seq)
					selected_seqs.append(sequence)
					phylp_seqs.append(sequence)
		selected_seqs.append('\n')
		phylp_seqs.append('\n')
		seq_full = ''.join(selected_seqs)
		phylp_seq_full = ''.join(phylp_seqs)
		with open(fna_save_file, 'a') as organism_append:
			organism_append.write(orga_id)
			organism_append.write(seq_full)
		with open(phylp_save_file, 'a') as phylp_append:
			phylp_append.write(phylp_id)
			phylp_append.write(phylp_seq_full)

	phylp_header_save_file = output_directory + 'all_organisms_header.phylip'
	phylp_header_file = open(phylp_header_save_file, 'w')
	phylp_header_file.close()
	phylp_header = str(organism_number) + ' ' + str(len(phylp_seq_full) - 1) + '\n' #subtract 1 because of new line character
	with open(phylp_header_save_file, 'a') as f: f.write(phylp_header)

	filenames = [phylp_header_save_file, phylp_save_file]
	full_phylp_output = output_directory + 'all_organisms_full.phylip'
	with open(full_phylp_output, 'w') as outfile:
	    for fname in filenames:
	        with open(fname) as infile:
	            for line in infile:
	                outfile.write(line)
	os.remove(phylp_header_save_file)
	os.remove(phylp_save_file)
	

all_fna_contstucter(BMGE_list, organism_list,sys.argv[1], sys.argv[2])



