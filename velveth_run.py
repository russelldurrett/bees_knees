import sys, os, glob, subprocess

'''
usage: velveth_run.py sample_list.txt
'''
#Sample Text should be unique identifiers for each data set. So App2_1_GCCAATAT_L001_R1_001.fastq.gz and App2_1_GCCAATAT_L001_R2_001.fastq.gz would be represented as App2_1

old_names = open(sys.argv[1]).readlines()
names = []
for name in old_names: 
	names.append(name.rstrip())

print 'working with these samples:'
print names 

fastq_list = glob.glob('*.gz')
print 'All fastq files:'
print fastq_list

for sample in names: 
	print 'working on '+ sample 
	sample_name = sample 
	sample_fastqs = [filename for filename in fastq_list if sample_name in filename]
#	sample_fastqs = [f for f in sample_fastqs]
	print 'found these fastqs: ' + ' '.join(sample_fastqs)
	args_str = '../tools/velvet_1.2.10/velveth ' + str(sample_name) + ' 95 -fastq.gz -shortPaired ' + str(sample_name) + '_merged.fastq.gz'
	print args_str
	args = str.split(args_str)
	print args
	subprocess.call(args)
	
