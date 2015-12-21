import sys, os 

''' 
usage: python genome_assembly_setup.py sample_list.txt, insert, sd, output_dir
''' 
# sample_list.txt should be unique identifiers for each data set. So App2_1_GCCAATAT_L001_R1_001.fastq.gz and App2_1_GCCAATAT_L001_R2_001.fastq.gz would be represented as App2_1
# Should be working in the folder where the fastqs are located
# insert is insert size and sd is standard deviation
# output_dir should be your output directory i.e. /home/russ/drew/masurca/


old_names = open(sys.argv[1]).readlines()
names = []
for name in old_names: 
	names.append(name.rstrip())

print 'working with these samples:'
print names 

config_header = """
DATA 
"""

config_footer = """ 
END
PARAMETERS
#this is k-mer size for deBruijn graph values between 25 and 101 are supported, auto will compute the optimal size based on the read data and GC content
GRAPH_KMER_SIZE = auto
#set this to 1 for Illumina-only assemblies and to 0 if you have 1x or more long (Sanger, 454) reads, you can also set this to 0 for large data sets with high jumping clone coverage, e.g. >50x
USE_LINKING_MATES = 0
#this parameter is useful if you have too many jumping library mates. Typically set it to 60 for bacteria and 300 for the other organisms 
LIMIT_JUMP_COVERAGE = 300
#these are the additional parameters to Celera Assembler.  do not worry about performance, number or processors or batch sizes -- these are computed automatically. 
#set cgwErrorRate=0.25 for bacteria and 0.1<=cgwErrorRate<=0.15 for other organisms.
CA_PARAMETERS = cgwErrorRate=0.15 ovlMemory=4GB
#minimum count k-mers used in error correction 1 means all k-mers are used.  one can increase to 2 if coverage >100
KMER_COUNT_THRESHOLD = 1
#auto-detected number of cpus to use
NUM_THREADS = 21
#this is mandatory jellyfish hash size -- a safe value is estimated_genome_size*estimated_coverage
JF_SIZE = 200000000
#this specifies if we do (1) or do not (0) want to trim long runs of homopolymers (e.g. GGGGGGGG) from 3' read ends, use it for high GC genomes
DO_HOMOPOLYMER_TRIM = 0
END
"""
d = os.getcwd()
fastq_list = os.listdir(d)
print fastq_list 
d = d + '/'



for sample in names: 
	print 'working on '+ sample 
	sample_name = sample 
	sample_fastqs = [filename for filename in fastq_list if sample_name in filename]
	sample_fastqs = [d + f for f in sample_fastqs]
	print 'found these fastqs: ' + ' '.join(sample_fastqs)
	sample_line = 'PE= pe ' + sys.argv[2] + ' ' + sys.argv[3] + ' ' + ' '.join(sample_fastqs)
	print sample_line 
	config_file = config_header + sample_line + config_footer
	print config_file
	print 'writing config file'
	outhandle = sys.argv[4] + '/' + sample + '.MaSuRCA.config.txt'
	outfile = open(outhandle, 'w')
	outfile.write(config_file)
	outfile.close()






