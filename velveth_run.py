import sys, os, glob, subprocess

#Outputs directories named after the sample and the kmer length used for velvetg to act upon

'''
usage: velveth_run.py sample_list.txt, kmer, filetype, readcategory, velvetdirectory
'''
# Sample list should be unique identifiers for each data set. So App2_1_GCCAATAT_L001_R1_001.fastq.gz and App2_1_GCCAATAT_L001_R2_001.fastq.gz would be represented as App2_1
#and each identifier should be on its own line
# Should be working in the directory containg the sequences you want to run, for example if you have interleaved data in the directory /genomes_batch1_merged you should run this
#in that directory
# kmer is the kmer length to be used
# filetype of data i.e. fastq, fasta, etc
# readcategory is the type of reads velvet can accept, short, long, shortPaired, longPaired, etc.
# velvetdirectory is the pathway to the proper velvet directory, i.e. /home/user/velvet_1.2.10

old_names = open(sys.argv[1]).readlines()
names = []
for name in old_names: 
	names.append(name.rstrip())

print 'working with these samples:'
print names 

#.fastq is working with fastqs (or whatever the format the sequence data is in), .gz if working with zipped files
fastq_list = glob.glob('*.' + sys.argv[3])
print 'All ' + sys.argv[3] + ' files:'
print fastq_list

for sample in names: 
	print 'working on '+ sample 
	sample_name = sample 
	sample_fastqs = [filename for filename in fastq_list if sample_name in filename]
	print 'found these fastqs: ' + ' '.join(sample_fastqs)
	args_str = sys.argv[5] + '/velveth ' + str(sample_name) + '_' + sys.argv[2] + ' ' + sys.argv[2] + ' -' +  sys.argv[3] + ' -' + sys.argv[4] + ' ' + str(sample_name) + '_interleaved.fastq'
	print args_str
	args = str.split(args_str)
	print args
	subprocess.call(args)
	
