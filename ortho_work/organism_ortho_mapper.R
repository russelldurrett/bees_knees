#Requires organism_ortho_sorter.R to be run first, creates a graph of all pairwise combinations of organisms
#which shows the number of orthologs they share

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

#upload rast_id, sample_id, species conversion table
#conversion_table = read.csv('rast_ids.csv',
#                            header = TRUE)

conversion_table = read.xlsx('rast_ids.xlsx', 1)

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
file_list = list.files(path = paste0(species, '_results', '/'), pattern = '\\orthologs_e.csv') #generate list of orthologs per organism files
organism_list = read.csv(paste0(species, '_results', '/', file_list[1]), header = TRUE)
colnames(organism_list)[2] <- toString(conversion_subset[1,1])
for (i in 2:length(file_list)){
  temp_org = read.csv(paste0(species, '_results', '/', file_list[i]), header = TRUE)
  colnames(temp_org)[2] <- toString(conversion_subset[i,1])
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
names(organism_listing) <- name_list #name the empty slots the organism rast IDs
for (names1 in name_list){
  organism_listing[[names1]] <- organism_list[[names1]] #Append a vector of the the ortholog genes for each organism to the list with its name being that of the organism
}

organism_listing <- lapply(organism_listing, function(x) unlist(x[!is.na(x)])) #remove NAs from the lists

nms <- combn( names(organism_listing) , 2 , FUN = paste0 , collapse = "+" , simplify = FALSE )

#for (z in 1:species_number){
#  rast_id <- toString(conversion_subset[z,1]) #replace the rast_ids with sample_ids for identification purposes going forward
#  sample_id <- toString(conversion_subset[z,2])
#  nms <- gsub(rast_id, sample_id, nms)
#}

organism_listing_comb <- combn( organism_listing , 2 , simplify = FALSE )
organism_pairs <- lapply( organism_listing_comb , function(x) length( intersect( x[[1]] , x[[2]] ) ) )
organism_pairs <- setNames( organism_pairs , nms )
organism_pairs_matrix <- matrix(unlist(organism_pairs), nrow = length(organism_pairs), byrow = TRUE)
organism_pairs_df <- data.frame(organism_pairs_matrix, stringsAsFactors=FALSE)
rownames(organism_pairs_df) <- nms #name the rows after the combinations of organisms
organism_pairs_df <- add_rownames(organism_pairs_df, 'pairs') #move the combination name to a column
colnames(organism_pairs_df)[2] <- 'shared_counts' #rename the column showing the number of shared genes
###*****************************


###*****************************
#CREATE FIGURES
plot1.1 = ggplot(data = organism_pairs_df, aes(x = pairs, y = shared_counts, fill = pairs)) + geom_bar(stat = 'identity', width = .5, position = position_dodge(width = 2)) + ggtitle('Shared Genes between Organism Pairs') + labs(x = 'Organism Pairs', y = 'Number of Genes Shared') + theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1)) + guides(fill=FALSE)
plot1.1
plot1.2 = ggplot(data = organism_pairs_df, aes(x = pairs, y = shared_counts, fill = pairs)) + geom_bar(stat = 'identity', width = .9, position = position_dodge(width = 1)) + ggtitle('Shared Genes between Organism Pairs Blended') + labs(x = 'Organism Pairs', y = 'Number of Genes Shared') + theme(axis.text.x=element_blank()) + guides(fill=FALSE)
plot1.2
###*****************************

###*****************************
#SAVE DATA FRAMES AND FIGURES
ggsave(paste0(species,'_results','/plot1.1.pdf'), plot = plot1.1)
ggsave(paste0(species,'_results','/plot1.2.pdf'), plot = plot1.2)
###*****************************