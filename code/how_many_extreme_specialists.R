library(nlme)
library(geiger)
require(phytools)
library(MASS)

phfiles<-as.character(list.files(path="../data/Corrected_Matrices/Plant_herbivore_matrices", full.names=TRUE, pattern="*.csv"))
ppfiles<-as.character(list.files(path="../data/Corrected_Matrices/Stouffer_Ecology_Matrices", full.names=TRUE, pattern="*.csv"))
planttree=read.newick("../data/plant_phylogeny/dated_tree.new")

#### Directory of species names and networks
speciesnames=read.table('../data/plant_phylogeny/corrected_names.tsv',header=TRUE,sep=',')

# Set up the results storage table
result_table=matrix(nrow=length(c(phfiles,ppfiles)),ncol=9,data=1000)
colnames(result_table)=c("network","network_type","spec_plants","spec_animals","gen_plants","gen_animals","n_plants","n_animals","plants_in_tree")

for(n in 1:length(c(phfiles,ppfiles))){
  file=c(phfiles,ppfiles)[n]
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

  pdeg=colSums(numeric_matrix)
  adeg=rowSums(numeric_matrix)

  n_in_tree=length(which(colnames(network_matrix) %in% planttree$tip.label))

  special_plants=as.numeric(length(which(pdeg==1)))
  special_animals=as.numeric(length(which(adeg==1)))
  general_plants=as.numeric(length(which(pdeg>1)))
  general_animals=as.numeric(length(which(adeg>1)))

  if(!length(colnames(numeric_matrix))==special_plants+general_plants){
    print('error: plants')
    print(file)
  }
  if(!length(rownames(numeric_matrix))==special_animals+general_animals){
    print('error: animals')
    print(file)
  }


  result_table[n,1]=netname
  result_table[n,2]=nettype
  # result_table[n,3]=mean(reldeg)
  result_table[n,3]=special_plants
  result_table[n,4]=special_animals
  result_table[n,5]=general_plants
  result_table[n,6]=general_animals
  result_table[n,7]=as.numeric(length(colnames(numeric_matrix)))
  result_table[n,8]=as.numeric(length(rownames(numeric_matrix)))
  result_table[n,9]=as.numeric(n_in_tree)
  # if((as.numeric(result_table[n,3])+as.numeric(result_table[n,5]))!=1){
  #   print('proportion error')
  #   print((as.numeric(result_table[n,3])+as.numeric(result_table[n,5])))
  # }
}

result_table=as.data.frame(result_table)

result_table$spec_plants=as.numeric(as.character(result_table$spec_plants))
result_table$spec_animals=as.numeric(as.character(result_table$spec_animals))
result_table$gen_plants=as.numeric(as.character(result_table$gen_plants))
result_table$gen_animals=as.numeric(as.character(result_table$gen_animals))
result_table$n_plants=as.numeric(as.character(result_table$n_plants))
result_table$n_animals=as.numeric(as.character(result_table$n_animals))


mod=glm(cbind(spec_animals,gen_animals) ~ network_type, result_table, family='binomial')

print(summary(mod))

mod2=glm(cbind(spec_plants,gen_plants) ~ network_type, result_table, family='binomial')

print(tapply((result_table$spec_animals/result_table$n_animals),result_table$network_type,mean))
print(tapply((result_table$spec_animals/result_table$n_animals),result_table$network_type,sd))

# result_table=as.data.frame(result_table)
# result_table$plants=as.numeric(as.character(result_table$plants))
# result_table$animals=as.numeric(as.character(result_table$animals))

# means=tapply(result_table$animals,result_table$network_type,mean)
# SEs=sqrt(tapply(result_table$animals,result_table$network_type,var)/tapply(result_table$animals,result_table$network_type,length))

# ph=result_table$animals[which(result_table$network_type=='ph')]
# pp=result_table$animals[which(result_table$network_type=='pp')]
# t_test=t.test(pp,ph,var.equal=FALSE)

# print(t_test)