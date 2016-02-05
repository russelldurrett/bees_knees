#This script is designed to create background genenomic profile (of bee gut bacteria) and then gain insight into the speific variation
#in the genomic profiles or specific organisms when compared to the whole.


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
library('clusterProfiler')
###*****************************