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
fastq_list = glob.glob('*.gz')
print 'All fastq files:'
print fastq_list

for sample in names: 
	print 'working on '+ sample 
	sample_name = sample 
	sample_fastqs = [filename for filename in fastq_list if sample_name in filename]
	print 'found these fastqs: ' + ' '.join(sample_fastqs)
	# Change pathway to get to your velvet directory
	# Second part of the string assumes your directory is named as the identifier in sample_list.txt, this is what velveth_run.py is defaulted as
	# The third part of the string is velvetg options which can be changed at will, just makes sure the sections begins with a space
	args_str = '../tools/velvet_1.2.10/velvetg ' + str(sample_name) + ' -ins_length 280 -exp_cov auto -cov_cutoff auto -min_contig_lgth 300'
	print args_str
	args = str.split(args_str)
	print args
	subprocess.call(args)