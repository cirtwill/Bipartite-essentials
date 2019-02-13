# library(ape)
# library(geiger)
# library(nlme)
# library(phytools)

source('helper_functions.R') 
# Contains functions for turning networks into binary matrices,
###########################################################################################################

phfiles<-as.character(list.files(path="../data/Corrected_Matrices/Plant_herbivore_matrices", full.names=TRUE, pattern="*.csv"))
ppfiles<-as.character(list.files(path="../data/Corrected_Matrices/Stouffer_Ecology_Matrices", full.names=TRUE, pattern="*.csv"))

# Here I'll count up how many species we're getting in each family.
network_sizes=matrix(nrow=length(phfiles)+length(ppfiles),ncol=3)

for(n in 1:length(c(phfiles,ppfiles))){
  file=c(phfiles,ppfiles)[n]
  net=gsub("../data/Corrected_Matrices/","",file) # Type of network, network name
  netname=gsub("_corrected.csv","",net)                     # same without .csv

  if(file%in%phfiles){
    nettype='ph'} else {
    nettype='pp'}

  # Read in network matrix, convert it to a numeric one
  network_matrix=read.csv(file,header=TRUE,sep=',',row.names=1)
  numeric_matrix=make_numeric_matrix(network_matrix)

  nplants=ncol(network_matrix)
  nanimals=nrow(network_matrix)
  network_sizes[n,]=c(netname,nplants,nanimals)  
}

network_sizes=as.data.frame(network_sizes)
colnames(network_sizes)=c("network","n_plants","n_animals")
network_sizes$n_plants=as.numeric(as.character(network_sizes$n_plants))
network_sizes$n_animals=as.numeric(as.character(network_sizes$n_animals))
network_sizes$total_species=network_sizes$n_plants+network_sizes$n_animals

print(network_sizes)
# write.table(families_by_network,file='../data/Jaccard/families_to_networks/families_by_network.csv',sep=',')
