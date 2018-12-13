library(car)
require(lme4)


networks<-as.character(list.files(path="../data/Jaccard/Random_Matrices/test", full.names=TRUE, pattern="*"))
# Distance from the observed, overlaps from the randoms
for(network in networks){
# out_table_single_J<-matrix(nrow=length(networks),ncol=999)
# out_table_single_S<-matrix(nrow=length(networks),ncol=999)
# n=1
  netname=gsub('../data/Jaccard/Random_Matrices/test',"",network)
  if(network %in% networks[1:59]){
    obsfile=paste0('../data/Jaccard/Overlap_dist/Stouffer_Ecology_Matrices/',netname,'_dist.csv',sep='')
  } else {
    obsfile=paste0('../data/Jaccard/Overlap_dist/Plant_herbivore_matrices/',netname,'_dist.csv',sep='')    
  }
  obsdata=read.csv(obsfile,header=TRUE,row.names=1,check.names=FALSE,sep=',')
  out_table_J<-matrix(nrow=99,ncol=1)
  out_table_S<-matrix(nrow=99,ncol=1)
  print(network)
  for(i in 1:99){
#      tryCatch({
#       unshared=read.csv(paste0(network,'/',netname,'_',i,'_notshared.csv',sep=''),header=TRUE,row.names=1,sep=',')
#       animals=read.csv(paste0(network,'/',netname,'_',i,'_animals.csv',sep=''),header=TRUE,row.names=1,sep=',')
#       interactions=read.csv(paste0(network,'/',netname,'_',i,'_interactions.csv',sep=''),header=TRUE,row.names=1,sep=',')
#       # print(c(nrows(unshared)==nrows(animals),nrows(unshared)==nrows(interactions),nrows(animals)==nrows(interactions)))
#       if(!nrow(unshared)==nrow(animals)){
#         print(i)
#       }
#       },
#               error = function(e) {print(i);NaN})
# }}
    print(i)
    animals=read.csv(paste0(network,'/',netname,'_',i,'_animals.csv',sep=''),header=TRUE,row.names=1,sep=',')
    interactions=read.csv(paste0(network,'/',netname,'_',i,'_interactions.csv',sep=''),header=TRUE,row.names=1,sep=',')
    unshared=read.csv(paste0(network,'/',netname,'_',i,'_notshared.csv',sep=''),header=TRUE,row.names=1,sep=',')

    # Need to filter out the bad comparisons in all of the above. Should be able to just compare rownames with obsdata
    lim_animals<-matrix(nrow=0,ncol=ncol(animals))
    lim_interactions<-matrix(nrow=0,ncol=ncol(animals))
    lim_unshared<-matrix(nrow=0,ncol=ncol(animals))
    names=c()
    for(rowname in rownames(animals)){
      plant1=strsplit(rowname,':')[[1]][1]
      plant2=strsplit(rowname,':')[[1]][2]
      if(rowname%in%rownames(obsdata)){
        lim_animals<-rbind(lim_animals,animals[rowname,])
        lim_interactions<-rbind(lim_interactions,interactions[rowname,])
        lim_unshared<-rbind(lim_unshared,unshared[rowname,])
        names=cbind(names,rowname)
      } else {
        altname=paste0(plant2,':',plant1)
        if(altname%in%rownames(obsdata)){
          lim_animals<-rbind(lim_animals,animals[rowname,])
          lim_interactions<-rbind(lim_interactions,interactions[rowname,])
          lim_unshared<-rbind(lim_unshared,unshared[rowname,])
          names=cbind(names,altname)
        }
      }
    }
    rownames(lim_animals)<-names
    rownames(lim_interactions)<-names
    rownames(lim_unshared)<-names
    # Alphabetize everything
    lim_animals<-lim_animals[order(rownames(lim_animals)),]
    lim_interactions<-lim_interactions[order(rownames(lim_interactions)),]
    lim_unshared<-lim_unshared[order(rownames(lim_unshared)),]
    obsdata<-obsdata[order(rownames(obsdata)),]

    # Now we can run the regressions
    R1Jaccard=glm(cbind(lim_animals[,1],lim_unshared[,1])~scale(obsdata$distance),family="binomial")    
    R1Sorenson=glm(cbind(lim_interactions[,1],lim_unshared[,1])~scale(obsdata$distance),family="binomial") 
    out_table_J[i,1]=R1Jaccard$coefficients['scale(obsdata$distance)']
    out_table_S[i,1]=R1Sorenson$coefficients['scale(obsdata$distance)']
    # out_table_single_J[n,i]=R1Jaccard$coefficients['scale(obsdata$distance)']
    # out_table_single_S[n,i]=R1Sorenson$coefficients['scale(obsdata$distance)']
    # for(j in 1:500){
    #   RRJaccard=glm(cbind(lim_animals[,j+1],lim_unshared[,j+1])~scale(obsdata$distance),family="binomial")
    #   RRSorenson=glm(cbind(lim_interactions[,j+1],lim_unshared[,j+1])~scale(obsdata$distance),family="binomial") 
    #   # I am using the first column to get null distributions for the observed
    #   # All subsequent columns are for testing type 1 and type 2 error.
    #   out_table_J[i,j+1]=RRJaccard$coefficients['scale(obsdata$distance)']
    #   out_table_S[i,j+1]=RRSorenson$coefficients['scale(obsdata$distance)']      
    # }
  }
  write.table(out_table_J,file=paste0('../data/Jaccard/Random_Regressions/test/',netname,'_randomCoeffs_Jaccard.tsv',sep=''),sep='\t')
  write.table(out_table_S,file=paste0('../data/Jaccard/Random_Regressions/test/',netname,'_randomCoeffs_Sorenson.tsv',sep=''),sep='\t')
    # n=n+1
}
# write.table(out_table_single_J,file='../data/Jaccard/Random_Regressions/allR1Coeffs_Jaccard.tsv',sep='\t')
# write.table(out_table_single_S,file='../data/Jaccard/Random_Regressions/allR1Coeffs_Sorenson.tsv',sep='\t')
