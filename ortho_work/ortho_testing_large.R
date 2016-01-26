
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
species = 'snogdrassella'

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


max_genes <- max(count.fields(filename))
input_groups = read.table(file = filename,
              col.names = 1:max_genes, #ADD ONE?
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

#Delimit the conversion_table
species_delim = str_sub(species,2, -1)
conversion_subset <- conversion_table[grep(species_delim, conversion_table$species), ]
assembly_delim = paste0('_',str_sub(assembly,1,1))
conversion_subset <- conversion_subset[grep(assembly_delim, conversion_subset$sample_id), ]
###*****************************


###*****************************
#CREATE DATA FRAMES SHOWING WHAT ORTHOLOGOUS GENES ARE PRESENT FOR EVERY SPECIES AND OF HOW MANY SPECIES CONTAIN EACH ORTHOLOGOUS GENE

#find rows where each species is present
species_number = nrow(conversion_subset)
gene_number = ncol(input_groups) #should be equal to max_genes
for (x in 1:species_number){
  for (i in 1:gene_number){
    gene_id_call = paste0('gene_',i)
    var_name = paste0('species_ortholog_rows_',x,'_',i)
    delimer = toString(conversion_subset[x,1])
    assign(var_name, input_groups[grep(delimer, input_groups[[gene_id_call]]), ])
  }
}

#combine data frames into one for each for species, showing every row (from the input file) where the species is present
for (x in 1:species_number){
  combined_data_frame = paste0(x,'_species_orthologs_combined')
  combined_data_frame_r = paste0(x,'_species_orthologs_combined_reduced')
  combined_data_frame_r_rn = paste0(x,'_species_orthologs_combined_reduced_rn')
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
  
  assign(combined_data_frame_r_rn, final_list) #Make a data frame with row names as a column named rn
  
  rnames_final_list <- final_list$rn
  rownames(final_list) <- rnames_final_list
  final_list$rn <-NULL
  
  assign(combined_data_frame_r, final_list) #make a data frame of all rows were the certain species has a gene present with row names
}

df = do.call(what=rbind,args=mget(paste0(1:species_number,"_species_orthologs_combined_reduced_rn")))
test = ddply(.data=df,.variables=colnames(df),.fun=nrow)
for (j in 1:gene_number){
  col_removal = paste0('gene_',j)
  test[col_removal] <-NULL
}

assign('gene_occurence_df', test) #data frame where an orthologous gene is next to the number of species which contain that gene

###*****************************

###*****************************
#DATA FRAMES SHOWING NUMBER OF GENES THAT ARE SHARED BY A CERTAIN NUMBER SPECIES
occurence_list = c()
shared_num_list = c()

for (k in 1:species_number){
  assign(paste0(k,'_gene_occurence_df'), filter(gene_occurence_df, V1 == k))
  assign(paste0(k,'_occurences'), nrow(get(paste0(k,'_gene_occurence_df'))))
  conversion_var = get(paste0(k,'_occurences'))
  shared_num_list = c(shared_num_list, k)
  occurence_list = c(occurence_list, conversion_var)
}

genes_in_species_df = data.frame(shared_num_list, occurence_list) #data frame showing how many genes are shared by any number of of the species
###*****************************


###*****************************
#FIGURE CONSTRUCTION
ggplot(gene_occurence_df, aes(factor(V1))) + geom_bar() + ggtitle('Shared Genes') + labs(x = 'Number of Species', y = 'Number of Genes')

###*****************************










