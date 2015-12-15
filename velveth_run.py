import sys, os, glob, subprocess

'''
usage: velveth_run.py sample_list.txt
'''
#Sample Text should be unique identifiers for each data set. So App2_1_GCCAATAT_L001_R1_001.fastq.gz and App2_1_GCCAATAT_L001_R2_001.fastq.gz would be represented as App2_1
#and each identifier should be on its own line
#Should be working in the directory containg the sequences you want to run, for example if you have interleaved data in the directory /genomes_batch1_merged you should run this
#in that directory

old_names = open(sys.argv[1]).readlines()
names = []
for name in old_names: 
	names.append(name.rstrip())

print 'working with these samples:'
print names 

#.fastq is working with fastqs (or whatever the format the sequence data is in), .gz if working with zipped files
fastq_list = glob.glob('*.fastq')
print 'All fastq files:'
print fastq_list

for sample in names: 
	print 'working on '+ sample 
	sample_name = sample 
	sample_fastqs = [filename for filename in fastq_list if sample_name in filename]
#	sample_fastqs = [f for f in sample_fastqs]
	print 'found these fastqs: ' + ' '.join(sample_fastqs)
	# Change pathway to get to your velvet directory
	# THe second part of the string sequence names the directory with the name from the sample_list.txt
	# The number in the third part of the string is the kmer length and can be changed (if testing multiple kmer lengths it would be worth it to include a identifier on the directory name)
	# This could be done by adding + '_95' after the first str(sample+name)
	# The rest of the third part of the string is velveth options which can be changed at will, just makes sure the sections begins and ends with a space
	# Add .gz if working with unzipped fastqs (or whatever file format) from the part of the string sequence
	args_str = '../tools/velvet_1.2.10/velveth ' + str(sample_name) + ' 95 -fastq.gz -shortPaired ' + str(sample_name) + '_merged.fastq'
	print args_str
	args = str.split(args_str)
	print args
	subprocess.call(args)
	
