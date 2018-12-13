# Read in the overlap data files (made by overlap_vs_distance.R)
files1<-as.character(list.files(path="../data/Jaccard/Overlap_dist/Plant_herbivore_matrices", full.names=TRUE, pattern="*.csv"))
files2<-as.character(list.files(path="../data/Jaccard/Overlap_dist/Stouffer_Ecology_Matrices", full.names=TRUE, pattern="*.csv"))

files=c(files1,files2)

overlap_data <- list()
for(network in files){
  netname=gsub('../data/Jaccard/Overlap_dist/',"",network)
  subfolder=strsplit(strsplit(netname,'-')[[1]][1],'/')[[1]][1]
  if(subfolder=='Stouffer_Ecology_Matrices'){
    nettype='pp'  } else {
      nettype='ph'   }

  message(paste0("Processing '",netname,"' "),appendLF=FALSE)

  overlap_data[[netname]]=read.csv(network,header=TRUE,row.names=1,check.names=FALSE,sep=',')
  overlap_data[[netname]]$network <- netname
  overlap_data[[netname]]$nettype <- nettype

  message("Done")
}

all_data <- do.call("rbind", overlap_data)
for(r in 1:nrow(all_data)){
  sp=strsplit(rownames(all_data)[r],'.csv.')[[1]][2]
  all_data$sp1[r]=strsplit(sp,':')[[1]][1]
  all_data$sp2[r]=strsplit(sp,':')[[1]][2]
}
all_data$fam1="quirk"
all_data$fam2="quirk"

# Read in the file that has the correct families
taxonomy=read.table('../data/plant_phylogeny/inputs_to_outputs.tsv',header=TRUE,sep='\t')
for(r in 1:nrow(taxonomy)){
  taxonomy$family[r]=strsplit(as.character(taxonomy$Output[r]),'/')[[1]][1]
  taxonomy$genus[r]=strsplit(as.character(taxonomy$Output[r]),'/')[[1]][2]
  taxonomy$species[r]=strsplit(as.character(taxonomy$Output[r]),'/')[[1]][3]
  taxonomy$name[r]=paste0(taxonomy$genus[r],'_',taxonomy$species[r])

}

for(sp in levels(as.factor(all_data$sp1))){
  for(r in 1:nrow(taxonomy)){
    if(sp==taxonomy$name[r]){
      fam=taxonomy$family[r]
    }
  } 
  for(s in 1:nrow(all_data)){
    if(all_data$sp1[s]==sp){
      all_data$fam1[s]=fam
    }
    if(all_data$sp2[s]==sp){
      all_data$fam2[s]=fam
    }
  }
}

# Composition per network:
families_by_network=matrix(nrow=length(files),ncol=201)
famlist=levels(as.factor(c(all_data$fam1,all_data$fam2)))
colnames(families_by_network)=famlist
for(r in 1:length(files)){
  net=levels(as.factor(all_data$network))[r]
  subset=all_data[which(all_data$network==net),]
  species=c(subset$sp1,subset$sp2)
  families=c(subset$fam1,subset$fam2)
  # Just unique species, family combos
  joint=unique(cbind(species,families))
  comp=tapply(joint[,2],joint[,2],length)
  for(c in 1:201){
    fam=famlist[c]
    if(fam %in% names(comp)){
      families_by_network[r,c]=comp[fam]
    } else {
      families_by_network[r,c]=0
    }
  }
}
colnames(families_by_network)[which(famlist=="quirk")]="''"
rownames(families_by_network)=levels(as.factor(all_data$network))
write.table(families_by_network,'../data/Jaccard/families_to_networks/families_by_network.csv',sep=',')


# List of pairs by family, within-family pairs only:


