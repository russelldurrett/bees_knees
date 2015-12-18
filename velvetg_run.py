import sys, os, glob, subprocess

'''
usage: velveth_run.py sample_list.txt, ins_length, exp_cov, cov_cutoff, min_contig_lgth, velvetdirectory
'''

#Sample Text should be unique identifiers for each data set. So App2_1_GCCAATAT_L001_R1_001.fastq.gz and App2_1_GCCAATAT_L001_R2_001.fastq.gz would be represented as App2_1
#and each identifier should be on its own line
#Should be working in the directory containg the sequences you want to run, for example if you have interleaved data in the directory /genomes_batch1_merged you should run this
#in that directory
# ins_length
# exp_cov
# cov_cutoff
# min_contig_length
# velvetdirectory is the pathway to the proper velvet directory, i.e. /home/user/velvet_1.2.10

old_names = open(sys.argv[1]).readlines()
names = []
for name in old_names: 
	names.append(name.rstrip())

print 'working with these samples:'
print names 

d = os.getcwd()
directory_list_all = os.listdir(d)
print directory_list_all
directory_list = [k for k in directory_list_all if '.' not in k]
print 'All directories:'
print directory_list

for sample in names: 
	print 'working on '+ sample 
	sample_name = sample 
	sample_directory = [filename for filename in directory_list if sample_name in filename]
	# Change pathway to get to your velvet directory
	# Second part of the string assumes your directory is named as the identifier in sample_list.txt, this is what velveth_run.py is defaulted as
	# The third part of the string is velvetg options which can be changed at will, just makes sure the sections begins with a space
	args_str = sys.argv[6] + '/velvetg ' + ' '.join(sample_directory) + ' -ins_length ' + sys.argv[2] +  ' -exp_cov ' + sys.argv[3] + ' -cov_cutoff ' + sys.argv[4] + ' -min_contig_lgth ' + sys.argv[5]
	print args_str
	args = str.split(args_str)
	print args
	subprocess.call(args)