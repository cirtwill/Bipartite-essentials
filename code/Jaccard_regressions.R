library(car)
require(lme4)

files1<-as.character(list.files(path="../data/Jaccard/Overlap_dist/Plant_herbivore_matrices", full.names=TRUE, pattern="*.csv"))
files2<-as.character(list.files(path="../data/Jaccard/Overlap_dist/Stouffer_Ecology_Matrices", full.names=TRUE, pattern="*.csv"))

files=c(files1,files2)

outtab=matrix(nrow=length(files),ncol=6)
colnames(outtab)=c('network','Jaccard_slope','Jaccard_p','Sorenson_slope','Sorenson_p','n_pairs')
combi=matrix(nrow=0,ncol=6)

for(n in 1:length(files)){
  network=files[n]
  netname=gsub('../data/Jaccard/Overlap_dist/',"",network)
  net=gsub('_dist.csv',"",netname)
  netdata=read.csv(network,header=TRUE,row.names=1,check.names=FALSE,sep=',')
  Jaccard=glm(cbind(n_shared_animals,n_notshared)~scale(distance),data=netdata,family="binomial")
  Sorenson=glm(cbind(n_shared_interactions,n_notshared)~scale(distance),data=netdata,family="binomial")
  size=nrow(netdata)

  obs_slopes=c(Jaccard$coefficients['scale(distance)'],summary(Jaccard)$coefficients['scale(distance)',4],Sorenson$coefficients['scale(distance)'],summary(Sorenson)$coefficients['scale(distance)',4])
  outtab[n,]=c(net,obs_slopes,size,C)

  if(n<12){
  	netdata$nettype='ph'
  } else {
  	netdata$nettype='pp'
  }
  print(n)
  netdata$network=netname
  combi=rbind(combi,netdata)
  print(outtab[n,])

}

combi$nettype=as.factor(combi$nettype)
fullreg=glm(cbind(n_shared_animals,n_notshared)~scale(distance)*nettype,data=combi,family="binomial")

outfile=paste0('../data/Jaccard/Observed_Regression/observed_coefficients.tsv')
write.table(outtab,file=outfile,sep='\t')
message("Done observed")

fullreg_bynetwork=glmer(cbind(n_shared_animals,n_notshared)~scale(distance)*nettype+(1+scale(distance)|network),data=combi,family="binomial")
fixes=summary(fullreg_bynetwork)$coefficients
ranes=ranef(fullreg_bynetwork)$network
write.table(fixes,file='../data/Jaccard/Observed_Regression/overall_bynetwork_reg_unranked_scaled_fixef.tsv')
write.table(ranes,file='../data/Jaccard/Observed_Regression/overall_bynetwork_reg_unranked_scaled_ranef.tsv')

outtab=as.data.frame(outtab)
outtab$Jaccard_slope=as.numeric(as.character(outtab$Jaccard_slope))
outtab$Jaccard_p=as.numeric(as.character(outtab$Jaccard_p))
outtab$Sorenson_slope=as.numeric(as.character(outtab$Sorenson_slope))
outtab$Sorenson_p=as.numeric(as.character(outtab$Sorenson_p))
outtab$nettype=c(rep('PH',11),rep('PP',59))
outtab$nettype=as.factor(outtab$nettype)
outtab$n_pairs=as.numeric(as.character(outtab$n_pairs))
# I think it may be best to make observed slopes, random slopes, and random-random slopes separately?
source('how_many_extreme_specialists.R')
outtab$network=as.character(droplevels(outtab$network))
result_table$network=as.character(droplevels(result_table$network))
outtab<-outtab[order(outtab$network),]
result_table<-result_table[order(result_table$network),]
outtab$C=result_table$C

slope_test=with(outtab,glm(Jaccard_slope~nettype*n_pairs))
pval_test=with(outtab,glm(Jaccard_p~nettype*n_pairs))
pptab=outtab[which(outtab$nettype=='PP'),]
# Significant positive effect of size and negative interaction with nettype==PP
PP_slope_test=with(pptab,glm(Jaccard_slope~n_pairs))
PP_pval_test=with(pptab,glm(Jaccard_p~n_pairs))


stupidCtest=with(outtab,glm(Jaccard_slope~nettype*C))

