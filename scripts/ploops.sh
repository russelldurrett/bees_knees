
#Set to directory where the files are located
cd ~/Github/bees_knees/ortho_work/bacteroidetes_gene_fnas

#Change to needed filetype, For example, .fna for performing muscle alignment, or .muscle for the trimming via BMGE
set files = `ls *.fna`

foreach i ($files)
	java -jar ~/GitHub/bees_knees/BMGE-1.12/BMGE.jar -i $i -t DNA -of $i".muscle"

end


#Change the set files ir line in the loop depending on alignment or trimming

#For alignment via muscle:
							#line 6: set files = `ls *.fna` 
							#line 9: muscle -in $i  -out $i".muscle"
#For trimming via BMGE: 
							#line 6: set files = `ls *.muscle` 
							#line 9: java -jar ~/GitHub/bees_knees/BMGE-1.12/BMGE.jar -i $i -t DNA -of $i".BMGE" - ~/GitHub/bees_knees/BMGE-1.12/BMGE.jar  <-should be set to the location of the BMGE.jar file
