import sys, os, glob, subprocess

'''
usage: quast_run.py sample_list.txt kmer
'''

#Sample Text should be unique identifiers for each data set. So App2_1_GCCAATAT_L001_R1_001.fastq.gz and App2_1_GCCAATAT_L001_R2_001.fastq.gz would be represented as App2_1
#and each identifier should be on its own line
#Should be working in the directory containg the directories of the assembled data

old_names = open(sys.argv[1]).readlines()
names = []
for name in old_names: 
	names.append(name.rstrip())

print 'working with these samples:'
print names 

args_str = '../quast-3.2/quast.py '
for sample in names: 
	print 'working on '+ sample 
	sample_name = sample 
	# Change pathway to get to your quast directory, assumes the directory is named as presented in the sample_list.txt and contigs file is contigs.fa
	args_str = args_str + str(sample_name)+ '_' + sys.argv[2] + '/contigs.fa '
	print args_str
args = str.split(args_str)
print args
subprocess.call(args)