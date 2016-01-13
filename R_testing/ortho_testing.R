
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
library('tidyr')
library('stringr')
###*****************************



###*****************************
# INITIAL INPUTS

#Species to work on? - bacteroidetes - gilliamella - snogdrassella - unknown -
species = 'bacteroidetes'

#assembly? - masurca - velvet -
assembly = 'masurca'
###*****************************


###*****************************
#INITIAL DATA SETUP

#upload rast_id, sample_id, species conversion table
conversion_table = read.csv('rast_ids.csv',
                            header = TRUE)

#upload orthologs
filename = paste0(species,'_jan11/OrthologousGroups.txt')

input_groups = read.table(file = filename,
              col.names = 1:37,
              fill = TRUE)


#rename rows, assuming the first row is what you want to rename the rows to
rnames <- input_groups[,1]
rownames(input_groups) <- rnames
input_groups$X1 <-NULL

#rename columns
for (i in 1:36){
  name  = paste0('gene_',
                 i)
  colnames(input_groups)[i] <- name
}

#Delimit the conversion_table
species_delim = str_sub(species,2, -1)
conversion_subset <- conversion_table[grep(species_delim, conversion_table$species), ]
assembly_delim = paste0('_',str_sub(assembly,1,1))
conversion_subset <- conversion_subset[grep(assembly_delim, conversion_subset$sample_id), ]
###*****************************

#find rows where each species is present
species_number = nrow(conversion_subset)
gene_number = ncol(input_groups)
for (x in 1:species_number){
  for (i in 1:gene_number){
    gene_id_call = paste0('gene_',i)
    var_name = paste0('species_ortholog_rows_',x,'_',i)
    delimer = toString(conversion_subset[x,1])
    assign(var_name, input_groups[grep(delimer, input_groups[[gene_id_call]]), ])
  }
}

#combine data frames into one for each for species, showing every row where the species is present
for (x in 1:species_number){
  combined_data_frame = paste0(x,'_species_orthologs_combined')
  combined_data_frame_r = paste0(x,'_species_orthologs_combined_reduced')
  #data_frame_list = c()
  list_1 <- get(paste0('species_ortholog_rows_',x,'_1'))
  list_2 <- get(paste0('species_ortholog_rows_',x,'_2'))
  assign(combined_data_frame, rbind(list_1, list_2))
  for (i in 3:(gene_number)){
    new_data_frame = get(paste0('species_ortholog_rows_',x,'_',i))
    #data_frame_list = c(data_frame_list, first_data_frame)
    old_data_frame = get(combined_data_frame)
    assign(combined_data_frame, rbind(old_data_frame, new_data_frame))
  }
  final_list <- get(combined_data_frame)
  final_list <- add_rownames(final_list, "rn")
  final_list <- final_list[grep(':$', final_list[['rn']]), ]
  
  rnames_final_list <- final_list$rn
  rownames(final_list) <- rnames_final_list
  final_list$rn <-NULL
  
  assign(combined_data_frame_r, final_list)
}






