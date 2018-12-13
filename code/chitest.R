library(nlme)
library(geiger)
require(phytools)

# Read in the overlap data files (made by overlap_vs_distance.R)
phfiles<-as.character(list.files(path="../data/Corrected_Matrices/Plant_herbivore_matrices", full.names=TRUE, pattern="*.csv"))
ppfiles<-as.character(list.files(path="../data/Corrected_Matrices/Stouffer_Ecology_Matrices", full.names=TRUE, pattern="*.csv"))

files=c(phfiles,ppfiles)

files1<-as.character(list.files(path="../data/Overlap_dist/Plant_herbivore_matrices", full.names=TRUE, pattern="*.csv"))
files2<-as.character(list.files(path="../data/Overlap_dist/Stouffer_Ecology_Matrices", full.names=TRUE, pattern="*.csv"))

altfiles=c(files1,files2)
overlap_data <- list()
for(network in altfiles){
  netname=gsub('../data/Corrected/',"",network)
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

#### Build the tree
planttree=read.newick("../data/plant_phylogeny/dated_tree.new")
collapsed_tree=collapse.singles(planttree)   #Collapses non-branching nodes (i.e., internal nodes on lines leading to only 1 species)

#### Directory of species names and networks
speciesnames=read.table('../data/plant_phylogeny/corrected_names.tsv',header=TRUE,sep=',')
speciesnames$new_lower=tolower(speciesnames$new_names)
speciesnames$original_lower=tolower(speciesnames$original_name)
# Remove all problematic characters
speciesnames$original_lower=gsub('  ', ' ', speciesnames$original_lower)
speciesnames$original_lower=gsub('_', ' ', speciesnames$original_lower)
speciesnames$original_lower=gsub('-', ' ', speciesnames$original_lower)
speciesnames$original_lower=gsub("'", ' ', speciesnames$original_lower)

# # Set up the chi-square table
chitable=matrix(nrow=length(files),ncol=length(levels(speciesnames$family)),data=0)
colnames(chitable)=levels(speciesnames$family)

#### Split the pairs 100x
for(n in 1:length(files)){
  file=files[n]
  print(file)
  netname=gsub('../data/Corrected_Matrices/','',file)

  if(file%in%phfiles){
    nettype='ph'} else {
    nettype='pp'}

  network_matrix=read.csv(file,header=TRUE,sep=',',row.names=1)
  if('X'%in%colnames(network_matrix)){          # Trim any superfluous columns
    network_matrix$X=NULL    }

  numeric_matrix=matrix(nrow=nrow(network_matrix),ncol=ncol(network_matrix))
  #Ensure all columns are numeric
  for(i in 1:nrow(network_matrix)){
    for(j in 1:ncol(network_matrix)){
      if(as.numeric(as.character(network_matrix[i,j]))>0){
        numeric_matrix[i,j]=1      }
      if(as.numeric(as.character(network_matrix[i,j]))==0){
        numeric_matrix[i,j]=0      }
        }}

  rownames(numeric_matrix)=rownames(network_matrix)
  colnames(numeric_matrix)=colnames(network_matrix)
  # colnames are plants

  fammat=matrix(nrow=ncol(numeric_matrix),ncol=2)
  colnames(fammat)=c("species","family")

  r=1
  for(sp in colnames(numeric_matrix)){
  	if(length(as.vector(strsplit(sp,'_ph_'))[[1]])==2){
    species=strsplit(sp,'_ph_')[[1]][1]
  	} else {
    species=strsplit(sp,'_m_pl_')[[1]][1]
	  }
	  spec=gsub('_',' ',species)

		tax=subset(speciesnames,speciesnames$original_lower==spec)
		# If necessary, try again with underscores included
		if(dim(tax)[1]==0){
		  tax=subset(speciesnames,speciesnames$original_lower==species)
		  }
		fammat[r,1]=species
		fammat[r,2]=as.character(tax$family[1])
		r=r+1
	}  

	famresults=as.data.frame(t(tapply(fammat[,2],fammat[,2],length)))
	for(colname in colnames(famresults)){
		chitable[n,colname]=famresults[,colname]
		}
}

chitable=chitable[,which(colSums(chitable)>0)]
chitable=chitable[,which(!colnames(chitable)=="unidentified")]
chisq.test(chitable)

# Restrict to families represented by more than 10 species
rest_chitable=chitable[,which(colSums(chitable)>10)]
chisq.test(rest_chitable)

# In both cases, families are really, really unevenly represented.