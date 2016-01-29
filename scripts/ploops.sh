
#Set to directory where the files are located
cd ~/Github/bees_knees/ortho_work/bacteroidetes_gene_fnas

#Change to needed filetype, For example, .fna for nucleotide fastas or .muscle for output of muscle, or .BMGE for the trimming
set files = `ls *.muscle`

foreach i ($files)
	java -jar ~/GitHub/bees_knees/BMGE-1.12/BMGE.jar -i $i -t DNA -of $i".BMGE"

end


#Change line in the loop depending on the command
#For alignment via muscle: muscle -in $i  -out $i".muscle"
#For trimming via BMGE: java -jar ~/GitHub/bees_knees/BMGE-1.12/BMGE.jar -i $i -t DNA -of $i".BMGE" - ~/GitHub/bees_knees/BMGE-1.12/BMGE.jar should be set to the location of the BMGE.jar file




#	filter_taxa_from_otu_table.py -i $i -o $i".biom" -n p__Firmicutes,p__Bacteroidetes,p__Actinobacteria,p__Proteobacteria,p__Spirochaetes,p__Acidobacteria,p__Chlorobi,p__Chloroflexi,p__Cyanobacteria,p__Deferribacteres,p__FBP,p__Fibrobacteres,p__Gemmatimonadetes,p__Lentisphaerae,p__Planctomycetes,p__Tenericutes,p__Verrucomicrobia

#	pick_otus.py -i $i -o picked_otus_97 -s 0.97
#	make_otu_table.py -i $i -o $i".biom"

# 	ProtBankExplorer -p $i -d ../Loki/Lokiarch.faa

##muscle -in $i  -out $i".muscle"
##hmmbuild --informat afa $i".hmm" $i 
#sig_rec_samp_AB.muscle
#	hmmsearch --domtblout $i."loki" $i ../Loki/Lokiarch.faa

##hmmsearch --domtblout $i.fasta $i.hmm ../Database/eukaryotes.faa
# BMGE -i $i -t DNA -of $i".BMGE"
##hmm_id_extractor.py $i $i".text"
##ret2aliv3.pl PRO $i
## BMGE -i $i -t AA -m BLOSUM30 -o $i".BMGE"
## phyml3 -i $i -d aa -m LG 
# ProtBankExplorer -p $i -d Gapicola_w_outgroups.fna
## taxid2tree.pl 

