#Find the Orthologs that are contained in every organism and also contain no paralogs

###*****************************
# INITIAL COMMANDS TO RESET THE SYSTEM

rm(list = ls())
if (is.integer(dev.list())){dev.off()}
cat("\014")

#Set working directory
setwd('/Users/dvanderwood/Github/bees_knees/ortho_work/')
###*****************************



###*****************************
# INSTALL LIBRARIES
library('dplyr')
library('plyr')
library('tidyr')
library('stringr')
library('ggplot2')
library('xlsx')
###*****************************


###*****************************
# INITIAL INPUTS

#Species to work on? - bacteroidetes - gilliamella - snogdrassella - unknown -
species = 'gilliamella'

#Data OrthoFinder was run? - jan11 - etc -
date = 'jan11'

#assembly? - masurca - velvet -
assembly = 'masurca'
###*****************************

###*****************************
#INITIAL DATA SETUP

#Upload table with rast ids
conversion_table = read.xlsx('rast_ids.xlsx', 1)

#upload gene_occurence data frame, which shows in how many species does an ortholog appear
gene_occurence_df <- read.csv(paste0(species, '_results/gene_occurence_df_e.csv'), header = TRUE)
gene_occurence_df$X <- NULL

#upload orthologs
filename = paste0(species,'_',assembly,'_',date,'/OrthologousGroups.txt')


max_genes <- max(count.fields(filename))
input_groups = read.table(file = filename,
                          col.names = 1:max_genes, 
                          fill = TRUE)

#rename rows, assuming the first row is what you want to rename the rows to
rnames <- input_groups[,1]
rownames(input_groups) <- rnames
input_groups$X1 <-NULL

#rename columns
for (i in 1:max_genes-1){ 
  name  = paste0('gene_',
                 i)
  colnames(input_groups)[i] <- name
}

input_original = input_groups #make a second copy of the original input fie so the input_groups data frame can be modified

#Delimit the conversion_table
species_delim = str_sub(species,2, -1)
conversion_subset <- conversion_table[grep(species_delim, conversion_table$species), ]
assembly_delim = paste0('_',str_sub(assembly,1,1))
conversion_subset <- conversion_subset[grep(assembly_delim, conversion_subset$sample_id), ]

species_number = nrow(conversion_subset)
gene_number = ncol(input_groups)
###*****************************



###*****************************
#CUT DOWN TO ORTHOLOGS THAT DON"T HAVE MORE GENES THAN ORGANISMS
paralog_containing <- paste0('gene_',(species_number+1)) #Find orthologs which don't have more than genes than there organisms, so if there are 3 organisms, orthologs with more than 3 genes are removed
input_groups <-  input_groups[!input_groups[[paralog_containing]]!='',] #If there are more genes than organisms, there must be a paralog

emptycols <- colSums(input_groups == "") == nrow(input_groups) #Remove empty columns
input_groups <- input_groups[!emptycols]

last_gene_col <- paste0('gene_',species_number) #Remove any orthologs which don't have at the least the number of organisms as genes, so 3 organisms, there needs to be at least 3 genes
input_groups <- input_groups[!input_groups[[last_gene_col]]=='',]

gene_occurence_df_all_organisms <- gene_occurence_df[gene_occurence_df$V1 == species_number,] #Find orthologs that contain all organisms

gene_occurence_df_all_organisms_list <- gene_occurence_df_all_organisms$rn

input_groups <- add_rownames(input_groups, "rn") #move the row names to a column named rn
input_groups_trimmed_rn <- subset(input_groups, rn %in% gene_occurence_df_all_organisms_list) #Remove any orthologs that don't have all the organisms in them

input_groups_trimmed <- input_groups_trimmed_rn
rnames_input_groups_trimmed <- input_groups_trimmed$rn # Next lines change the column rn back into row names and saves it
rownames(input_groups_trimmed) <- rnames_input_groups_trimmed
input_groups_trimmed$rn <-NULL
###*****************************

###*****************************
#SAVE DATA FRAME OF ORTHOLOGS WHICH ARE CONTAINED IN ALL ORGANISMS AND DO NOT CONTAIN ANY PARALOGS

write.csv(input_groups_trimmed, file = paste0(species,'_results/all_organism_orthologs.csv'), row.names = TRUE)
###*****************************



