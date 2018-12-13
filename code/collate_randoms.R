
files1<-as.character(list.files(path="../data/Jaccard/Overlap_dist/Plant_herbivore_matrices", full.names=TRUE, pattern="*.csv"))
files2<-as.character(list.files(path="../data/Jaccard/Overlap_dist/Stouffer_Ecology_Matrices", full.names=TRUE, pattern="*.csv"))

files=c(files1,files2)


obs_vs_random=matrix(nrow=length(files),ncol=1000)
obsdata=read.table('../data/Jaccard/Observed_Regression/observed_coefficients.tsv')
# I think I will just do Jaccards for now - not 100% sure why I cared about Sorenson
obs_vs_random[,1]=obsdata$Jaccard_slope

# And let's collect the p-values for ran vs ran-ran here
ran_vs_ranran=matrix(nrow=length(files),ncol=999)

netnames=c()
for(n in 1:length(files)){
	print obsdata
  network=files[n]
  netname=strsplit(network,'/')[[1]][6]
  net=gsub('_dist.csv',"",netname)
  print(net)
  netnames=cbind(netnames,net)
	randdata=read.table(paste0('../data/Jaccard/Random_Regressions/',net,'_randomCoeffs_Jaccard.tsv'))
	obs_vs_random[n,2:1000]=t(randdata[,1])

	for(j in 1:999){
		ranrans=randdata[j,2:500]
		ran=randdata[j,1]
		p=length(ranrans[which(ranrans>ran)])/500
		ran_vs_ranran[n,j]=p
	}

}
obs_vs_random=as.data.frame(obs_vs_random)
colnames(obs_vs_random)[1]=c("Observed")
rownames(obs_vs_random)=netnames
write.table(obs_vs_random,file='../data/Jaccard/Observed_Regression/observed_vs_random.tsv')

ran_vs_ranran=as.data.frame(ran_vs_ranran)
rownames(ran_vs_ranran)=netnames
write.table(ran_vs_ranran,file='../data/Jaccard/Observed_Regression/random_vs_randomrandom.tsv')

obs_ps=matrix(nrow=length(files),ncol=2)
for(n in 1:length(files)){
	obs=obs_vs_random[n,1]
	rans=obs_vs_random[n,2:1000]
	p_greater=length(which(rans>obs))/999
	p_lesser=length(which(rans<obs))/999
	obs_ps[n,]=c(p_greater,p_lesser)
}
obs_ps=as.data.frame(obs_ps)
colnames(obs_ps)=c("greater","lesser")
rownames(obs_ps)=netnames

