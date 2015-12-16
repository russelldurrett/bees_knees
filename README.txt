de novo genome assembly pipeline using MaSuRCA 


Construct sample lists: 
	Assuming a directory, i.e. genomes, full of pair-ended reads, i.e. App2-1_GCCAATAT_L001_R1_001.fastq.gz and App2-1_GCCAATAT_L001_R2_001.fastq.gz
	Creat a list of of samples, App2-1_GCCAATAT_L001_R1_001.fastq.gz and App2-1_GCCAATAT_L001_R2_001.fastq.gz becomes App2-1
	Commands:
		cd ~/path/path/genomes
		ls | cut -d'_' -f 1 | sort | uniq -d > sample_list.txt

	This keeps everything in the file name before the first underscore, if you wanted the first two, change "-f 1" to "-f 1,2"


MaSuRCA

Copy your sample list into your masurca config folder:
	cp sample_list.txt ~/path/path/path/masurca_configs

Use masurca_config_generator.py to generate config files
	Arguements for python script:
		masurca_config_generator.py, sample_list.txt, insert, sd, output_dir
			insert = insert sizes
			sd = standard deviation of sizes
			output_dir = output directory path to store config files, the same directory you just copied your sample_list.txt to


Make Directories for each sample in your present directory:

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

Run Assemblies for each sample:

	for x in `ls`
	do
	cd $x
	./assemble.sh
	cd ../
	done