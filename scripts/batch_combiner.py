import sys, os, glob, subprocess

'''
usage: velveth_run.py sample_list.txt
'''

old_names = open(sys.argv[1]).readlines()
names = []
for name in old_names: 
	names.append(name.rstrip())

	# assumes the file names are at least kind of consistent, dif is batch2_1 is App2-1_S# and batch2_2 is App2-1

print 'working with these samples:'
print names 
for sample in names: 
	print 'working on '+ sample 
	sample_name = sample 
	sep = '_'
	rest = sample_name.split(sep, 1)[0]
	args_str = 'cat ' + '../genomes_batch2_1_merged/' + str(sample_name) + '_merged.fastq ' + '../genomes_batch2_2_merged/' + str(rest) + '_merged.fastq > ' + str(sample_name) + '_merged_cat.fastq'
	print args_str
	args = str.split(args_str)
	print args
	subprocess.call(args)