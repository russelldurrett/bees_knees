#This script will run the alignment and and trimming over all the fna files in a directory
#Intended to run over all the gene .fnas created by fna_parser_gene_constructer.py

#Set to directory where the files are located
cd ~/Github/bees_knees/ortho_work/bacteroidetes_gene_fnas

#Change to needed filetype, For example, .fna for performing muscle alignment, or .muscle for the trimming via BMGE
set files = `ls *.fna`

foreach i ($files)
	java -jar ~/GitHub/bees_knees/BMGE-1.12/BMGE.jar -i $i -t DNA -of $i".BMGE"

end


#Change the set files ir line in the loop depending on alignment or trimming

#For alignment via muscle: (assumes muscle is available in the path directory and can just be called with the command muscle, if not, modify it to the path to the muscle command)
							#line 8: set files = `ls *.fna` 
							#line 11: muscle -in $i  -out $i".muscle"
#For trimming via BMGE: 
							#line 8: set files = `ls *.muscle` 
							#line 11: java -jar ~/GitHub/bees_knees/BMGE-1.12/BMGE.jar -i $i -t DNA -of $i".BMGE" - ~/GitHub/bees_knees/BMGE-1.12/BMGE.jar  <-should be set to the location of the BMGE.jar file
