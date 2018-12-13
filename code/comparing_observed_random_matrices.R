# Comparing with random matrices

# Slopes in observed, random networks
obsran=read.table('../data/Jaccard/Observed_Regression/observed_vs_random.tsv')
# P-values in random vs. ranran
ranran=read.table('../data/Jaccard/Observed_Regression/random_vs_randomrandom.tsv')

obs_p=matrix(nrow=70,ncol=2)
for(i in 1:70){
	obs_p[i,1]=obsran[i,1]
	obs_p[i,2]=length(which(obsran[i,2:1000]<obsran[i,1]))
}

ranran$summary=rowMeans(ranran)

