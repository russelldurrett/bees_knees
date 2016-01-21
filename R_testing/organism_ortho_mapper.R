

#Requires organism_ortho_sorter.R to be run first

###*****************************
# INITIAL COMMANDS TO RESET THE SYSTEM

rm(list = ls())
if (is.integer(dev.list())){dev.off()}
cat("\014")

#Set working directory
setwd('/Users/dvanderwood/Github/bees_knees/R_testing/')
###*****************************


###*****************************
# INSTALL LIBRARIES
library('dplyr')
library('plyr')
library('tidyr')
library('stringr')
library('ggplot2')
###*****************************



###*****************************
# INITIAL INPUTS

#Species to work on? - bacteroidetes - gilliamella - snogdrassella - unknown -
species = 'bacteroidetes'

#Data OrthoFinder was run? - jan11 - etc -
date = 'jan11'

#assembly? - masurca - velvet -
assembly = 'masurca'
###*****************************


###*****************************
#INITIAL DATA SETUP

#upload rast_id, sample_id, species conversion table
conversion_table = read.csv('rast_ids.csv',
                            header = TRUE)

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

#upload organisms - ortholog data frames and combine
file_list = list.files(path = paste0(species, '_', assembly, '_', date, '/'), pattern = '\\orthologs_e.csv') #generate list of orthologs per organism files
organism_list = read.csv(paste0(species, '_', assembly, '_', date, '/', file_list[1]), header = TRUE)
colnames(organism_list)[2] <- conversion_subset[1,1]
for (i in 2:length(file_list)){
  temp_org = read.csv(paste0(species, '_', assembly, '_', date, '/', file_list[i]), header = TRUE)
  colnames(temp_org)[2] <- conversion_subset[i,1]
  organism_list <- merge(organism_list, temp_org, by='X', all.x = TRUE, all.y = TRUE)
}
organism_list$X = NULL #remove X column used to combine data frames
###*****************************

###*****************************
#FIND INTERSECTIONS BETWEEN ALL ORGANISM PAIRS

name_list <- colnames(organism_list)[1:species_number] #gather all the organism names in a list


#organism_listing <- list() #create an empty list
#for (names1 in name_list){ #Append a vector of the the ortholog genes for each organism to the list with its name being that of the organism
#  organism_listing[[names1]] <- organism_list[[names1]]
#}

#Same as above but more memory efficient apparently because the list does not grow and is the proper size at the start
organism_listing <- vector(mode='list', length = length(name_list)) #create an empty list of proper length
for (names1 in name_list){
  organism_listing1[[names1]] <- organism_list[[names1]] #Append a vector of the the ortholog genes for each organism to the list with its name being that of the organism
}

common_orthologs <- intersect(organism_list[,1],organism_list[,2])
common_orthologs <- common_orthologs[!is.na(common_orthologs)]
n = length(file_list)
organism_pairs = ((n*(n+1)/2) - n)


###*****************************







