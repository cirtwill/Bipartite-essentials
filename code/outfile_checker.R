source('helper_functions.R') 

# Checking to make sure each file has the requisite 3 output files

dirs<-as.character(list.files(path="../data/Jaccard/Random_Matrices", full.names=TRUE, pattern="*"))
# print(dirs)
for(n in 1:length(dirs)){

  subdir=dirs[n]
  print(subdir)
  files <- as.character(list.files(path=subdir,full.names=TRUE,pattern="*.csv"))
  if(length(files)!=3*999){
    print('not done')
    for(i in 900:999){
      outfiles=grep(paste0('_',i,'_',sep=''),files)      
      if(length(outfiles)!=3){
        print(i)
      }
    }
  }
}

