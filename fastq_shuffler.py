import sys, os, glob, subprocess

'''
usage: python fastq_shuffler.py sample_list.txt
'''

old_names = open(sys.argv[1]).readlines()
names = []
for name in old_names: 
	names.append(name.rstrip())

print 'working with these samples:'
print names 

#fastq_list = [f for f in os.listdir('.') if os.path.isfile(f)]
fastq_list = glob.glob('*.gz')
print 'All fastq files:'
print fastq_list

for sample in names: 
	print 'working on '+ sample 
	sample_name = sample 
	sample_fastqs = [filename for filename in fastq_list if sample_name in filename]
#	sample_fastqs = [f for f in sample_fastqs]
	print 'found these fastqs: ' + ' '.join(sample_fastqs)
	args_str = '../velvet_1.2.10/contrib/shuffleSequences_fasta/shuffleSequences_fastq.pl ' + ' '.join(sample_fastqs) + ' ../genomes_batch2_2_merged/' + str(sample_name) + '_merged.fastq.gz'
	print args_str
	args = str.split(args_str)
	print args
	p = subprocess.Popen(args, stdout=subprocess.PIPE)



#../velvet_1.2.10/contrib/shuffleSequences_fasta/shuffleSequences_fastq.pl App2_1_GCCAATAT_L001_R1_001.fastq.gz 
#App2_1_GCCAATAT_L001_R2_001.fastq.gz ../genomes_batch2_2_merged/App2_1GCCAATAT_merged.fastq.gz

