de novo genome assembly pipeline using MaSuRCA and Velvet


	Construct sample lists: 
		Assuming a directory, i.e. genomes, full of pair-ended reads, i.e. App2-1_GCCAATAT_L001_R1_001.fastq.gz and App2-1_GCCAATAT_L001_R2_001.fastq.gz
		Creat a list of of samples, App2-1_GCCAATAT_L001_R1_001.fastq.gz and App2-1_GCCAATAT_L001_R2_001.fastq.gz becomes App2-1
		Commands:
			cd ~/path/path/genomes
			ls | cut -d'_' -f 1 | sort | uniq -d > sample_list.txt
	
		This keeps everything in the file name before the first underscore, if you wanted the first two, change "-f 1" to "-f 1,2" It will be necessary to open this file and delete the line which 	contains the simply sample (created because the the sample_list.txt is in the folder). This can be done with a text editor or the vim command if working on a console.
		sample_list.txt is present as an example.
	
	
	MaSuRCA
	
		Copy your sample list into your masurca config folder:
			cp sample_list.txt ~/path/path/path/masurca_configs
	
		Use masurca_config_generator.py to generate config files in your curent directory
			Arguements for python script:
				masurca_config_generator.py, sample_list.txt, insert, sd, output_dir
					insert = insert sizes
					sd = standard deviation of sizes
					output_dir = output directory path to store config files, the same directory you just copied your sample_list.txt to
	
	
		Make Directories for each sample in your current directory:
	
			for x in `cat ~/path/path/masurca/sample_list.txt `
			do
			mkdir $x
			done
	
		Make assembly shells for each sample using the config files and place them in the folder for each sample:
	
			for x in `cat ~/path/path/masurca/sample_list.txt ` 
			do
			echo 'working on ' $x
			cd $x
			~/path/path/MaSuRCA-3.1.3/bin/masurca ~/path/path/masurca/$x*
			cd ../
			done
	
		Create Assemblies for each sample:
	
			for x in `ls`
			do
			cd $x
			./assemble.sh
			cd ../
			done
	
	
	Velvet For paired-end reads
	
		Assuming you already have created your sample_list.txt and it is in the directory with your sequence data.
	
			**If working with paired-end reads that are in separate files it is necessary to interleave the data for velvet.
	
		Interleave paired-end reads 
	
			Use sequence_shuffler.py
				Arguements for python script:
					sequence_shuffler.py sample_list.txt, filetype, velvetdirectory, output_dir
						filetype = filetype for sequence data, i.e. fastq, fasta
						velvetdirectory = location of your velvet directory, i.e. /home/user/velvet_1.2.10
						output_dir = the directory where you want the interleaved files to be saved, for example: make a directory named genomes_interleaved
	
		Create directories with velveth
			-directories will be created in the same folder as the interleaved files are
	
			Use velveth_run.py
				Arguements for python script:
					velveth_run.py sample_list.txt, kmer, filetype, readcategory, velvetdirectory
						kmer is the kmer length to be used
						filetype of data i.e. fastq, fasta, etc
						readcategory is the type of reads velvet can accept, short, long, shortPaired, longPaired, etc.
						velvetdirectory is the pathway to your velvet directory, i.e. /home/user/velvet_1.2.10
	
	
		Create Assemblies for each sample:
			-should be in the directory where the velveth directories were made (the same as the interleaved data)
	
			Use velvetg_run.py
				Arguements for python script:
					velveth_run.py sample_list.txt, ins_length, exp_cov, cov_cutoff, min_contig_lgth, velvetdirectory
						ins_length = velvetg arguement, the insert length for your sequence data
						exp_cov = velvetg arguement, i.e. auto
						cov_cutoff = velvetg arguement, i.e auto
						min_contig_length = velvetg arguement, usually equal to or slightly larger than ins_length
						velvetdirectory is the pathway to the proper velvet directory, i.e. /home/user/velvet_1.2.10


***Assuming Annotation is run on RAST, download .faa and .fna files.***

Finding ortholgous genes across species

	Run Orthofinder
		python orthofinder.py -f home/user/species_assembly -t 17
			-directory which contains the annotated
			-f is followed by the directory containing the genomes (assembled and annotated)
			-t is followed by the number of threads to be used


Find which orthologs each organism contains - Only works with single species data sets

		Create folders called called species_results for the outputs of the R codes to be placed into
			- to make the programs work on a group of multiple species, change the species part of this identifier to something unique and use that whenever species is called
				- the rast_ids.xlsx must also be identified as detailed below
	
		Output of orthofinder should be in a folder with the following naming convention "species_assembly_date" 
			- this will be the input for this program
			- this should be the case if the organisms are contained in a file named "species_assembly" before orthofinder is run
	
		A file called rast_ids.xlsx must be present in the working directory which contains three columns with information on the orgniams being processed
			- rast_id
			- sample_id
			- species
			- xlsx is used to preserve rast IDs which end in 0 (so the 0 is not dropped), this could be cirumvented with minor changes if you use a text file and read it as a table
			- To allow multi-species groups, this file should only contain the the exact organisms which will be worked on
				- the section in all the subsequent R codes dealing with deliminating the conversion table should be commented out and conversion_table should be set equal to conversion_subset
				- this is done because natively, the rast_id.xlsx file is assumed to contain information on more than the current specie that is being run and the program uses the input species to
					retain only the relevant subset of the table for each run
	
		organism_ortho_sorter.R
			- Construct csv files that show which orthologous genes each organsism contains and a plot showing the number of genes shared
			  by any number of organisms
			 - Inputs to be changed
				- species
				- date orthofinder was run
				- which assembly is being used
				- working directory
	
	
		organism_ortho_mapper.R
			- creates a graph of all pairwise combinations of organisms which shows the number of orthologs they share
			- Inputs are exactly the same as organism_ortho_sorter.R
			- Also, must be run after organism_ortho_sorter.R because it uses its outputs
	
		unique_ortho_finder.R
		 - Find the orthologs that are contained in every organism and also contain no paralogs
		 	- output as a table called all_organisms_orthologs.csv in the repsective results directory
		 - Same inputs as other R programs
	
	
Construct Gene FNAs for the common, paralog free orthologs of all organisms within a data set
	
	fna_parser_gene_constructer.py
		- This script will search through a directory of .fna files and using a list of common orthologs,
		  create new .fna files for each orhologous gene containing the the sequences for each organism.
		- Arguements for python script:
			fna_parser_gene_constructer.py fna_directory, shared_orthologs, output_directory
				fna_directory =  directory containing the fasta files you wish to parse, for example: bacteroidetes_annotated_fnas/	
				shared_orthologs = output of unique_ortho_finder.R, for example: bacteroidetes_results/all_organism_orthologs.csv
				output_directory = directory to save the new fnas to, for example: bacteroidetes_gene_fnas/
			
Align and Trim fna files for all the orthologous genes

	ploops.sh
		- This script will run the alignment and and trimming over all the fna files in a directory
		- Lines 5, 8, and 11 are modified depending on the step
		- Line 5 is set to the species_gene_fnas/ directory based on what species is being run
		- For alignment: Line 8: set files = `ls *.fna`
						 Line 11: muscle -in $i  -out $i".muscle" 
		- For trimming:  Line 8: set files = `ls *.muscle` 
						 Line 11: java -jar ~/GitHub/bees_knees/BMGE-1.12/BMGE.jar -i $i -t DNA -of $i".BMGE"
						 	- where the .jar part is the location of the BMGE command

Construct phyogenetic trees based on the orthologous genes
	
	organism_genome_reconstructer_by_species_fnas_phylips.py
		- This script will search through a directory of that contains .fna.muscle.BMGE files of single genes (composed of sequences from every organism for the data set)
		  and construct a phylip (and fna) file that contains aligned genomes of ortholgous genes for each organism.
		- Arguements for python script:
			organism_genome_reconstructer_by_species_fnas_phylips.py input_directory, output_directory
				input_directory = directory containing files you wish to parse, for example: bacteroidetes_gene_fnas/
				output_directory = directory to save the new fnas to, for example: bacteroidetes_all_fna					

	Run PhyML
	 - Parameters used in development, default unless otherwise stated
	 	- Data Type = DNA
		- Input sequences = sequential
		- Non parametric bootstrap analysis = 100
		- nucleotide substitution = GTR
		- Gamma distribution parameter = 4


Using a given gene, search a group of genomes via blast for similar genes
	
	gene_searcher_with_blast.py
		- This script will take in genomes (faas or fnas), create a local blast database and then
	   	  blast against the the database with a given sequence (in fasta format) and return all the genes (and by extension
	   	  organisms) which are similar (or contain similar genes).
		- Arguements for python script:
			gene_searcher_with_blast.py input_directory, output_directory, input_seq
				input_directory = directory containing fnas or faas for all organisms which you wish to search through for the given sequence, for example: bacteroidetes_fna/
				output_directory = directory where you wish to put the constructed blast database and blast search file and conmbined fna file, for example: bacteroidetes_search/
				input_seq = fasta file containing the sequence for which you wish to blast the organisms against, for example: carb_metabolism_gene.fasta

	blast_xml_parser
		- This script will parse through an xml blast output file and extract all the genes above a certain bitscore and write them out in a new csv file
		- Arguements for python script:
			blast_xml_parser.py input_xml, bit_score_cutoff
				input_xml = xml blast output file to parse
				bit_score_cutoff = lowest bit score to accept
			


Programs and Packages Used:
 - Working on a OSX environemt
 - Python
 - Velvet Assembler
 - MaSuRCA
 - Blast+
 - MCL graph clustering algorithm
 - Orthofinder
 - MUSCLE
 - BMGE
 - PhyML





