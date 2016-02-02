#This script takes in a directory of gbk files and a product name and then parses through the files
#pulling out the organisms and the corresponding genes which produce the input product


import Bio, sys, os, glob, csv, re

'''
usage: gbk_gene_product_searcher.py input_directory, product_type
'''

#input directory = location of the .gbk files
#product name to be searched for

from Bio import SeqIO

def gbk_list_maker(input_directory):
	#create new gbk files for each organism removing any hypotheical proteins
	#this will cut down on the number of products that will be searched through
	for root, dirs, files in os.walk(input_directory):
		gbk_list = [i for i in files if i.endswith('.gbk')]
		print gbk_list
	return gbk_list


gbk_list = gbk_list_maker(sys.argv[1])

def gene_finder(input_directory, gbk_list, product_type):
	for organism in gbk_list:
		filename = input_directory + organism
		gene_list= []
		for genome in SeqIO.parse(filename, 'genbank'):
			for i,feature in enumerate(genome.features):
			    if feature.type=='CDS':
			        if 'product' in feature.qualifiers: #verify it codes for a real protein (not pseudogene)
			            if feature.qualifiers['product'] != ['hypothetical protein']:
			            	gene_product = feature.qualifiers['product'][0]
			            	print gene_product
			            	#if product_type.lower() in gene_product.lower():
			            	#	print feature
			            	#	gene_list.append(genome)
			#genome.features = [f for f in genome.features if f.type == "CDS" and f.qualifiers['product'] != ['hypothetical protein']]
			#full_filename = input_directory + 'no_hypothetical_' + organism
			#SeqIO.write(genome, full_filename, "genbank")
		print genome
		full_filename = input_directory + 'found_' + product_type + '_' + organism
		SeqIO.write(genome, full_filename, "genbank")
		#organism_product_file= open(full_filename, 'w')
		#organism_product_file.close()
		#with open(full_filename, 'a') as organism_append:
		#	for k in gene_list:
		#		print k
		#		organism_append.write(k)



#gene_finder(sys.argv[1], gbk_list, sys.argv[2])
def fasta_converter(input_directory, gbk_list):
	for organism in gbk_list:
		print organism
		filename = input_directory + organism
		output_filename = input_directory + organism + '.fasta'
		print output_filename
		input_handle = open(filename, "rU")
		output_handle = open(output_filename, "w")
		 
		sequences = SeqIO.parse(input_handle, "genbank")
		count = SeqIO.write(sequences, output_handle, "fasta")
		 
		output_handle.close()
		input_handle.close()

#fasta_converter(sys.argv[1], gbk_list)











