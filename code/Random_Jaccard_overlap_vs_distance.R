library(ape)
library(geiger)
library(nlme)
library(phytools)

source('helper_functions.R') 

# Don't need the trees, just want to corral all the overlaps in the random and random-random matrices.

###########################################################################################################

dirs<-as.character(list.files(path="../data/Random_Matrices/test", full.names=TRUE, pattern="*"))
# print(dirs)

for(n in 1:length(dirs)){
  subdir=dirs[n]
  print(subdir)
  files <- as.character(list.files(path=subdir,full.names=TRUE,pattern="*.csv"))

  # if(length(files)==999){

  # print(length(files))
  # Make sure there's a receptacle directory
  altdir=gsub("../data/Random_Matrices/test/","",subdir) # Type of network, network name
  dir.create(paste0('../data/Jaccard/Random_Matrices/test/',altdir))
 
  for(z in 1:length(files)){
    netfile=files[z]
    # netfile=paste0('../data/Random_Matrices/M_PL_057/M_PL_057_',z,'_rand.csv')
    print(netfile)   
    # Read in network matrix, convert it to a numeric one
    network_matrix=read.csv(netfile,header=TRUE,sep=',',row.names=1)
    numeric_matrix=make_numeric_matrix(network_matrix)

    # make a list of all plant pairs in the community
    plantpairs=combn(colnames(numeric_matrix),2)
    # Fuck it, I'll shrink the pairs to the good list for Peralta and Bodner later.

    #build the results container for the network
    colls <- c("n_shared_animals","n_shared_interactions","n_notshared")
    # shared animals/not shared is Jaccard, shared interactions (shared aimals x2)/not shared is Sorenson
    # Going to want separate files for each of shared_animals, shared_interactions, notshared
    animals=matrix(data=0,nrow=ncol(plantpairs),ncol=501) # observed plus all randoms
    rownames(animals)=interaction(plantpairs[1,],plantpairs[2,],sep=':')
    interactions=matrix(data=0,nrow=ncol(plantpairs),ncol=501)
    rownames(interactions)=interaction(plantpairs[1,],plantpairs[2,],sep=':')
    notshared=matrix(data=0,nrow=ncol(plantpairs),ncol=501)
    rownames(notshared)=interaction(plantpairs[1,],plantpairs[2,],sep=':')

    #observed values
    for(p in 1:ncol(plantpairs)){
      plantpair=plantpairs[,p]                                            # store the pair locally for ease of use
      tippair=c(as.character(plantpair[1]),as.character(plantpair[2]))    # get the pair of associated tipnames

      # Get numbers of shared an unshared partners
      result <- calculate_overlap(numeric_matrix,plantpair)     # Intersection, union, notshared
      animals[p,1] <- result[1]
      interactions[p,1] <- 2*result[1]
      notshared[p,1] <- result[3]
      }

    randdir=gsub('_rand.csv','',netfile)
    rando=gsub('Random_Matrices','Random_Random_Matrices',randdir)
    randfiles=as.character(list.files(path=rando,full.names=TRUE,pattern="*.csv"))
    # Random values
    # for(q in 1:500){
    #   randfile=read.csv(randfiles[q],header=TRUE,sep=',',row.names=1)
    #   numeric_matrix=make_numeric_matrix(randfile)
  
    #   for(p in 1:ncol(plantpairs)){
    #     col=q+1
    #     plantpair=plantpairs[,p]                                            # store the pair locally for ease of use
    #     tippair=c(as.character(plantpair[1]),as.character(plantpair[2]))    # get the pair of associated tipnames

    #     # Get numbers of shared an unshared partners
    #     result <- calculate_overlap(numeric_matrix,plantpair)     # Intersection, union, notshared
    #     animals[p,col] <- result[1]
    #     interactions[p,col] <- 2*result[1]
    #     notshared[p,col] <- result[3]
    #     }
    #   file.remove(randfiles[q])
    # }
    # file.remove(netfile)

  shortname=strsplit(netfile,'/')[[1]][6]
  shorty=strsplit(shortname,'_rand')[[1]][1]
  print(shorty)
  outFileName1=paste('../data/Jaccard/Random_Matrices/test/',altdir,'/',shorty,'_animals.csv',sep='')
  outFileName3=paste('../data/Jaccard/Random_Matrices/test/',altdir,'/',shorty,'_interactions.csv',sep='')
  outFileName2=paste('../data/Jaccard/Random_Matrices/test/',altdir,'/',shorty,'_notshared.csv',sep='')

  write.table(animals,file=outFileName1,sep=',')
  write.table(interactions,file=outFileName2,sep=',')
  write.table(notshared,file=outFileName3,sep=',')

  }

  # }
}
