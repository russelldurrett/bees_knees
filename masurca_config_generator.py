import sys, os 

''' 
usage: python genome_assembly_setup.py sample_names.txt 
''' 

old_names = open(sys.argv[1]).readlines()
names = []
for name in old_names: 
	names.append(name.rstrip())

print 'working with these samples:'
print names 

config_header = """
PATHS
JELLYFISH_PATH=/home/rud2004/tools/MaSuRCA/MaSuRCA-1.9.4.CHIMP/bin
SR_PATH=/home/rud2004/tools/MaSuRCA/MaSuRCA-1.9.4.CHIMP/bin
CA_PATH=/home/rud2004/tools/MaSuRCA/MaSuRCA-1.9.4.CHIMP/CA/Linux-amd64/bin
END


DATA 
"""

config_footer = """ 
END

PARAMETERS
#this is k-mer size for deBruijn graph values between 25 and 101 are supported, auto will compute the optimal size based on the read data and GC content
GRAPH_KMER_SIZE=auto
#set this to 1 for Illumina-only assemblies and to 0 if you have 2x or more long (Sanger, 454) reads
USE_LINKING_MATES=1
#this parameter is useful if you have too many jumping library mates. Typically set it to 60 for bacteria and something large (300) for mammals
LIMIT_JUMP_COVERAGE = 60
#these are the additional parameters to Celera Assembler.  do not worry about performance, number or processors or batch sizes -- these are computed automatically. for mammals do not set cgwErrorRate above 0.15!!!
CA_PARAMETERS = ovlMerSize=30 cgwErrorRate=0.25 ovlMemory=4GB
#minimum count k-mers used in error correction 1 means all k-mers are used.  one can increase to 2 if coverage >100
KMER_COUNT_THRESHOLD = 1
#auto-detected number of cpus to use
NUM_THREADS= 22
#this is mandatory jellyfish hash size
JF_SIZE=100000000
#this specifies if we do (1) or do not (0) want to trim long runs of homopolymers (e.g. GGGGGGGG) from 3' read ends, use it for high GC genomes
DO_HOMOPOLYMER_TRIM=0
END
"""

fastq_list = os.listdir('/scratchLocal/masonlab/russ/Drew/FASTQS')
print fastq_list 




for sample in names: 
	print 'working on '+ sample 
	sample_name = sample 
	sample_fastqs = [filename for filename in fastq_list if sample_name in filename]
	sample_fastqs = ['/scratchLocal/masonlab/russ/Drew/FASTQS/' + f for f in sample_fastqs]
	print 'found these fastqs: ' + ' '.join(sample_fastqs)
	sample_line = 'PE= pe 280 60 ' + ' '.join(sample_fastqs)
	print sample_line 
	config_file = config_header + sample_line + config_footer
	print config_file
	print 'writing config file'
	outhandle = '/scratchLocal/masonlab/russ/Drew/CONFIGS/' + sample + '.MaSuRCA.config.txt'
	outfile = open(outhandle, 'w')
	outfile.write(config_file)
	outfile.close()






