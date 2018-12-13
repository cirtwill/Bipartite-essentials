library(Hmisc)
library(lme4)
library(vegan)

phfiles<-as.character(list.files(path="../data/Corrected_Matrices/Plant_herbivore_matrices", full.names=TRUE, pattern="*.csv"))
ppfiles<-as.character(list.files(path="../data/Corrected_Matrices/Stouffer_Ecology_Matrices", full.names=TRUE, pattern="*.csv"))

netslopes=matrix(nrow=length(c(phfiles,ppfiles)),ncol=3)
colnames(netslopes)=c("nettype","slope","p")

families_by_network=read.table('../data/Jaccard/families_to_networks/families_by_network.csv',header=TRUE,sep=',')
# Remove family-less species
families_by_network$'X..'<-NULL
# families with >20 species in all the dataset...
goodfams=families_by_network[,which(colSums(families_by_network)>20)]
goodfams$'Other'=rowSums(families_by_network)-rowSums(goodfams)

#Gather the observed slopes
fixeffs=read.table(paste('../data/Jaccard/Observed_Regression/observed_coefficients.tsv',sep=''))
rownames(netslopes)=fixeffs[,1]
netslopes[,1]=c(rep('ph',11),rep('pp',59))
netslopes[,2]=fixeffs[,2]
netslopes[,3]=fixeffs[,3]
netslopes=as.data.frame(netslopes)
netslopes[,2]=as.numeric(as.character(netslopes[,2]))
netslopes[,3]=as.numeric(as.character(netslopes[,3]))

fams=as.matrix(families_by_network)/rowSums(as.matrix(families_by_network))
famdist=vegdist(fams,method="bray")

goodnorm=as.matrix(goodfams)/rowSums(as.matrix(goodfams))
gooddist=vegdist(goodnorm,method="bray")

perm=adonis(famdist~netslopes[,2],strata=netslopes[,1],permutations=9999)
perm2=adonis(gooddist~netslopes[,2],strata=netslopes[,1],permutations=9999)

famassoc=cca(fams~netslopes[,2])
famassoc2=cca(goodnorm~netslopes[,2])
# Now see which of the goodfams are associated with the constraint axis.

familyconts=summary(famassoc)$species[,1] # correlation with slope = -1
familyconts=familyconts[order(familyconts)]
write.table(familyconts,file='../data/Jaccard/families_to_networks/family_CCA_positions.tsv',sep='\t')

write.table(perm$aov.tab,file='../data/Jaccard/families_to_networks/permanova_table.tsv',sep='\t')

familyconts2=summary(famassoc2)$species[,1]
familyconts2=familyconts2[order(familyconts2)]
write.table(familyconts2,file='../data/Jaccard/families_to_networks/limited_family_CCA_positions.tsv',sep='\t')

write.table(perm2$aov.tab,file='../data/Jaccard/families_to_networks/limited_permanova_table.tsv',sep='\t')

