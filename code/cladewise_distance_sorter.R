library(ape)
library(geiger)
library(nlme)
library(phytools)
library(lme4)

# This code takes the files describing overlap in interaction partners for each network, 
# stitches them together, and returns a file with overlap between species in the same clade
# (taken from the same network) across all networks

###########################################################################################################

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

###########################################################################################################

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

###########################################################################################################


# Now we want to create subsets based on families.
samefam=matrix(nrow=nrow(all_data),ncol=7)
colnames(samefam)=c(colnames(all_data),'family')
rownames(samefam)=rownames(all_data)

# A long process to make the names in the overlap file match the names in taxo
for(pair in rownames(all_data)){
  network=paste(all_data[pair,]$network,'.',sep='')
  net=strsplit(network,'/')[[1]][2]
  netty=paste('_',tolower(strsplit(net,'_dist.csv.')[[1]][1]),sep='')

  step1=strsplit(pair,network)[[1]][2]
  step2=strsplit(step1,':')[[1]]

  sp2=strsplit(pair,':')[[1]][2]
  long1=strsplit(pair,':')[[1]][1]
  inter=strsplit(long1,'/')[[1]][2]
  sp1=strsplit(inter,'.csv.')[[1]][2]
  # Y'know, I probably want to go with the phylomatic version of families. So use taxonomy names
  fam1=as.character(taxonomy[sp1,]$family)
  fam2=as.character(taxonomy[sp2,]$family)

# Now we can test whether two species are in the same family
if(as.character(fam1)==as.character(fam2)){
  samefam[pair,"family"]=as.character(fam1)
  # And store all the information.
  samefam[pair,"n_shared_animals"]=as.numeric(all_data[pair,"n_shared_animals"])
  samefam[pair,"n_shared_interactions"]=as.numeric(all_data[pair,"n_shared_interactions"])
  samefam[pair,"n_notshared"]=as.numeric(all_data[pair,"n_notshared"])
  samefam[pair,"distance"]=as.numeric(all_data[pair,"distance"])
  # not sure what I was up to with this rankdist thing
  # samefam[pair,"rankdist"]=as.numeric(all_data[pair,"rankdist"])
  samefam[pair,"network"]=as.character(all_data[pair,"network"])
  samefam[pair,"nettype"]=as.character(all_data[pair,"nettype"])    
  }
}

# Remove familyless species now

# Prepare the file for printing
samefam=as.data.frame(samefam)
samefam=subset(samefam,samefam$family!='NA')
samefam=subset(samefam,samefam$family!='unidentified')

# samefam$ll=as.numeric(as.character(samefam$ll))
# samefam$N=as.numeric(as.character(samefam$N))
# samefam$lXl=as.numeric(as.character(samefam$lXl))
# samefam$motifs=as.numeric(as.character(samefam$motifs))
# samefam$other=as.numeric(as.character(samefam$other))
# samefam$specialized=as.numeric(as.character(samefam$specialized))
# samefam$total=as.numeric(as.character(samefam$total))
# samefam$distance=as.numeric(as.character(samefam$distance))
# samefam$rankdist=as.numeric(as.character(samefam$rankdist))


write.table(samefam,file='../data/cladewise_overlap_dist.csv',sep=',',col.names=TRUE,row.names=TRUE)
