import sys, os, glob, subprocess

'''
usage: python fastq_shuffler.py sample_list.txt, filetype, shuffleSeq_loc, output_dir
'''

#Sample Text should be unique identifiers for each data set. So App2_1_GCCAATAT_L001_R1_001.fastq.gz and App2_1_GCCAATAT_L001_R2_001.fastq.gz would be represented as App2_1
#Should be working in the folder where the fastq.gz's (your sequence data) are located
#output_dir i.e. ../genomes_batch1_merged/
#filetype for shuffling i.e. fastq, fasta, etc
# shuffleSeq_loc the pathway to proper shuffeSequencer

old_names = open(sys.argv[1]).readlines()
names = []
for name in old_names: 
	names.append(name.rstrip())

print 'working with these samples:'
print names 


#.fastq is working with fastqs (or whatever the format the sequence data is in), .gz if working with zipped files
fastq_list = glob.glob('*.' + sys.argv[2])
print 'All fastq files:'
print fastq_list

for sample in names: 
	print 'working on '+ sample 
	sample_name = sample 
	sample_fastqs = [filename for filename in fastq_list if sample_name in filename]
	#sample_fastqs = [f for f in sample_fastqs]
	print 'found these fastqs: ' + ' '.join(sample_fastqs)
	#remove .gz if working with unzipped fastqs (or whatever file format), change pathway to get to your velvet directory and the directory where you want the interleaved sequences saved
	args_str = sys.argv[3] + ' ' + ' '.join(sample_fastqs) + ' ' + sys.argv[4] + '/' + str(sample_name) + '_interleaved.fastq'
	print args_str
	args = str.split(args_str)
	print args
	p = subprocess.Popen(args, stdout=subprocess.PIPE)



#../velvet_1.2.10/contrib/shuffleSequences_fasta/shuffleSequences_fastq.pl App2_1_GCCAATAT_L001_R1_001.fastq.gz 
#App2_1_GCCAATAT_L001_R2_001.fastq.gz ../genomes_batch2_2_merged/App2_1GCCAATAT_merged.fastq.gz

