library(ape)
library(geiger)
library(nlme)
library(phytools)

source('helper_functions.R') 
# Contains functions for turning networks into binary matrices,
###########################################################################################################

# Read in the file that has the correct families
taxinfo=read.table('../data/plant_phylogeny/inputs_to_outputs.tsv',header=TRUE,sep='\t')
taxinfo=as.data.frame(taxinfo)
taxonomy=taxinfo
taxonomy$Input<-NULL
taxonomy$family=1
taxonomy$genus=1
taxonomy$tipname=1
famjunk=strsplit(as.character(taxonomy$Output),split='/')
for(i in 1:nrow(taxonomy)){
  taxonomy$family[i]=famjunk[[i]][1]
  taxonomy$genus[i]=famjunk[[i]][2]
  taxonomy$tipname[i]=paste0(famjunk[[i]][2],'_',famjunk[[i]][3])
}
taxonomy<-taxonomy[which(duplicated(taxonomy)==FALSE),]
row.names(taxonomy)=taxonomy$tipname
# Can't have the rownames since c. 50 species are in more than one web.

###########################################################################################################
phfiles<-as.character(list.files(path="../data/Corrected_Matrices/Plant_herbivore_matrices", full.names=TRUE, pattern="*.csv"))
ppfiles<-as.character(list.files(path="../data/Corrected_Matrices/Stouffer_Ecology_Matrices", full.names=TRUE, pattern="*.csv"))

# Here I'll count up how many species we're getting in each family.
families=levels(as.factor(taxonomy$family))
families_by_network=matrix(nrow=length(c(phfiles,ppfiles)),ncol=length(families))
colnames(families_by_network)=families
rownames(families_by_network)=c(phfiles,ppfiles)

for(n in 1:length(c(phfiles,ppfiles))){
  file=c(phfiles,ppfiles)[n]
  net=gsub("../data/Corrected_Matrices/","",file) # Type of network, network name
  netname=gsub("_corrected.csv","",net)                     # same without .csv
  if(file %in% phfiles){
    planttree=read.newick(paste0('../data/plant_phylogeny/trees/',gsub('Plant_herbivore_matrices/','',netname),'.new'))
  } else {
    planttree=read.newick(paste0('../data/plant_phylogeny/trees/',gsub('Stouffer_Ecology_Matrices/','',netname),'.new'))
  }
  # Ensure all tip labels lower-case
  planttree$tip.label<-tolower(planttree$tip.label)
  # collapse non-branching nodes (i.e., internal nodes on lines leading to only 1 species)
  collapsed_tree=collapse.singles(planttree)

  # compute the distance matrix from this supertree
  plant_distances <- cophenetic.phylo(planttree)

  print(file)
  # duplicate row names in notovny

  if(file%in%phfiles){
    nettype='ph'} else {
    nettype='pp'}

  # Read in network matrix, convert it to a numeric one
  network_matrix=read.csv(file,header=TRUE,sep=',',row.names=1)
  numeric_matrix=make_numeric_matrix(network_matrix)

  # Make a list of families for this network
  famlist=matrix(nrow=length(colnames(network_matrix)),ncol=2)
  for(z in 1:length(colnames(numeric_matrix))){
    plant=colnames(network_matrix)[z]
    fam=as.character(taxonomy[plant,]$family)
    famlist[z,1]=plant
    famlist[z,2]=fam
  }

  lists=tapply(famlist[,2],famlist[,2],length)
  for(family in families){
    if(family!=""){
      if(family %in% names(lists)){
        families_by_network[n,family]=lists[family]
      } else {
        families_by_network[n,family]=0
      }
    }
  }

  # make a list of all plant pairs in the community
  # Can't have comparisons between 2 of: gleicheniaceae, dennstaedtiaceae, blechnaceae
  # cyatheaceae, dicksoniaceae, marattiaceae
  # Don't want comparisons with mystery species (those without families)
  # In Bodner and Peralta, don't want comparisons between 2 manually-added species.

  questionable_quomparisons=c('gleicheniaceae', 'dennstaedtiaceae', 'blechnaceae', 'cyatheaceae', 'dicksoniaceae', 'marattiaceae')

  plantpairs=combn(colnames(numeric_matrix)[which(taxonomy[colnames(numeric_matrix),]$family!="")],2)
  # Remove comparisons that will have overly long distances
  if(file %in% c('../data/Corrected_Matrices/Plant_herbivore_matrices/ph_bodner_2010_handmade_corrected.csv',"../data/Corrected_Matrices/Plant_herbivore_matrices/ph-peralta-2014-marlborough-metaweb_corrected.csv")){
    good_plantpairs=matrix(nrow=2,ncol=ncol(plantpairs))
    for(i in 1:ncol(plantpairs)){
      sp1=plantpairs[1,i]
      sp2=plantpairs[2,i]
      if(!taxonomy[sp1,]$family%in%questionable_quomparisons){
        good_plantpairs[,i]=plantpairs[,i]
      } else {
        if(!taxonomy[sp2,]$family%in%questionable_quomparisons){
          good_plantpairs[,i]=plantpairs[,i]
        } else {
          good_plantpairs[,i]=-1
        }
      }
    }
    plantpairs<-good_plantpairs[,which(good_plantpairs[1,]!=-1)]
  }


  #build the results container for the network
  colls <- c("n_shared_animals","n_shared_interactions","n_notshared","distance")
  # shared animals/not shared is Jaccard, shared interactions (shared aimals x2)/not shared is Sorenson
  networkres=matrix(data=0,nrow=ncol(plantpairs),ncol=length(colls))
  rownames(networkres)=interaction(plantpairs[1,],plantpairs[2,],sep=':')
  colnames(networkres)=colls

  # iterate over all pairs of plants
  for(p in 1:ncol(plantpairs)){
    plantpair=plantpairs[,p]                                            # store the pair locally for ease of use
    tippair=c(as.character(plantpair[1]),as.character(plantpair[2]))    # get the pair of associated tipnames
    networkres[p,"distance"] <- plant_distances[tippair[1],tippair[2]]  # add their phylogenetic distance

    # Get numbers of shared an unshared partners
    result <- calculate_overlap(numeric_matrix,plantpair)     # Intersection, union, notshared
    networkres[p,"n_shared_animals"] <- result[1]
    networkres[p,"n_shared_interactions"] <- 2*result[1]
    networkres[p,"n_notshared"] <- result[3]

  }

outFileName=paste('../data/Jaccard/Overlap_dist/',netname,'_dist.csv',sep='')

write.table(networkres,file=outFileName,sep=',')
  
}

write.table(families_by_network,file='../data/Jaccard/families_to_networks/families_by_network.csv',sep=',')
