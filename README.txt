de novo genome assembly pipeline using MaSuRCA and Velvet


Construct sample lists: 
	Assuming a directory, i.e. genomes, full of pair-ended reads, i.e. App2-1_GCCAATAT_L001_R1_001.fastq.gz and App2-1_GCCAATAT_L001_R2_001.fastq.gz
	Creat a list of of samples, App2-1_GCCAATAT_L001_R1_001.fastq.gz and App2-1_GCCAATAT_L001_R2_001.fastq.gz becomes App2-1
	Commands:
		cd ~/path/path/genomes
		ls | cut -d'_' -f 1 | sort | uniq -d > sample_list.txt

	This keeps everything in the file name before the first underscore, if you wanted the first two, change "-f 1" to "-f 1,2" It will be necessary to open this file and delete the line which contains the simply sample (created because the the sample_list.txt is in the folder). This can be done with a text editor or the vim command if working on a console.
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


Assuming Annotation is run on RAST, download .gbk, .faa, and .fna files.





