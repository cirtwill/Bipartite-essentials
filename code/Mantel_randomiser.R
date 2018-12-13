# 1. Observed shared/notshared for each network - Done
# 2. Generate 999 random shuffles for each network - Done.
# 3. Calculate shared/notshared for each random network
# 4. Generate 500 random shuffles for each 999 random shuffle - Done.
# 5. Calculate shared/notshared for each randomized random network
# 6. Calculate observed p-value
# 7. Calculate distribution of random p-values for each matrix

source('helper_functions.R')
###########################################################################################################
phfiles<-as.character(list.files(path="../data/Corrected_Matrices/Plant_herbivore_matrices", full.names=TRUE, pattern="*.csv"))
ppfiles<-as.character(list.files(path="../data/Corrected_Matrices/Stouffer_Ecology_Matrices", full.names=TRUE, pattern="*.csv"))

# for(n in 1:70){
for(n in 1:2){
  # file=c(phfiles,ppfiles)[n]
  file=ppfiles[n]
  print(file)

  network_matrix=read.csv(file,header=TRUE,sep=',',row.names=1)
  numeric_matrix=make_numeric_matrix(network_matrix)
  plantnames=colnames(numeric_matrix)

  net=gsub("../data/Corrected_Matrices/","",file)
  netname=gsub("_corrected.csv","",net)
  shortname=strsplit(netname,'/')[[1]][2]

  dir.create(paste0('../data/Random_Matrices/test/',shortname))
  # dir.create(paste0('../data/Random_Random_Matrices/',shortname))
  # Shuffle the plant names and write a new matrix
  for(z in 1:99){
    print(z)
    shuffnames=sample(plantnames)
    modmat=numeric_matrix
    colnames(modmat)=shuffnames

    outFileName=paste0('../data/Random_Matrices/test/',shortname,'/',shortname,'_',z,'_rand.csv')
    write.table(modmat,file=outFileName,sep=',',append=FALSE)

    #Make a directory for the 500 sub-randomisations
    # subdir=gsub('_rand.csv',"",outFileName)
    # subsubdir=gsub("Random_Matrices","Random_Random_Matrices",subdir)
    # dir.create(subsubdir)
    # for(q in 1:500){
    #     shuffnames=sample(plantnames)
    #     modmat2=numeric_matrix
    #     colnames(modmat2)=shuffnames

    #     outFileName2=paste0(subsubdir,'/',shortname,'_',z,'_',q,'_rand.csv')
    #     write.table(modmat2,file=outFileName2,sep=',')
    #   }
  }
}
