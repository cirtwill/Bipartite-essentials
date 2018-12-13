library(ape)
library(geiger)
library(nlme)
library(phytools)
library(lme4)
library(lmerTest)
library(car)

rm(list=ls(all=TRUE))

options(warn=2)

# From cladewise_distance_sorter.R
samefam=read.table('../data/cladewise_overlap_dist.csv',sep=',',header=TRUE)

which_test=matrix(nrow=1000,ncol=3)
what_scale=matrix(nrow=1000,ncol=3)

frankendata=matrix(nrow=0,ncol=ncol(samefam))
colnames(frankendata)=c("n_shared_animals","n_shared_interactions","n_notshared",
    "distance","network","nettype","family")

p_test=function(model){
  p_est=deltaMethod(model,"b1+b3",parameterNames=paste("b",0:3,sep=''))
  p_z=p_est$Estimate/p_est$SE
  p_p=2*pnorm(-abs(p_z))
  result=c(p_est,p_p)
  return(result)  
}

check_dataset=function(dataset){
  if(nrow(dataset)>1){ # Must have multiple rows, checking n per row seperately for multi-network families
      if(max(dataset$distance)-min(dataset$distance)>0.001){ # If there's range in distance
        if(max(dataset$n_shared_animals)-min(dataset$n_shared_animals)>=1){        # If there's a range in no-overlap motifs
          if(max(dataset$n_shared_interactions)-min(dataset$n_shared_interactions)>=1){              # If there's a range in partial-overlap motifs
            if(max(dataset$n_notshared)-min(dataset$n_notshared)>=1){        # If there's a range in total-overlap motifs
              return('ok')} else {
            return('reject') }
          } else {
            return('reject') }
        } else {
          return('reject') }
      } else {
        return('reject') }
  } else {
    return('reject')
  }
}

# If there's only one network, R refuses to fit NAs for nettype
print_glm_outputs=function(dataset,family,nettype){
  # print(c(family,'glm'))
  reg=glm(cbind(n_shared_animals,n_notshared)~scale(distance),data=dataset,family="binomial",maxit=1000)
  write.table(summary(reg)$coef,
    file=paste0('../data/Jaccard/families_to_networks/Regressions/',family,'_',nettype,'_reg_fixef.tsv'),sep='\t')
}

print_glmer_notype_outputs=function(dataset,fam,nettype){
  # print(c(family,'glmer'))
  reg=glmer(cbind(n_shared_animals,n_notshared)~scale(distance)+(1|network),data=dataset,family="binomial",
    control=glmerControl(optimizer="bobyqa",optCtrl=list(maxfun=100000000)))
  write.table(summary(reg)$coef,
    file=paste0('../data/Jaccard/families_to_networks/Regressions/',fam,'_',nettype,'_reg_fixef.tsv'),sep='\t')
}

select_model=function(dataset,family,i){
  dataset$network=as.factor(droplevels(dataset$network))
  dataset$nettype=as.factor(droplevels(dataset$nettype))
  if(length(levels(dataset$network))==1){
    test1="glm"
    test2="none"
    nettype=levels(dataset$nettype)[1]
    scala=scale(dataset$distance)
    print_glm_outputs(subdata,family,nettype)      
  } else {
    # Family in more than one network. 
    famdata=matrix(nrow=0,ncol=ncol(dataset))          # Make a dummy dataset to keep the good networks
    networks=levels(dataset$network)
    # Check whether each network has 2+ rows, keep only the good ones
    for(network in networks){
      netdata=dataset[which(dataset$network==network),] 
      tested=check_dataset(netdata)
      if(tested=="ok"){
        famdata=rbind(famdata,netdata)
      }
    }
    if(check_dataset(famdata)=="ok"){
    famdata=as.data.frame(famdata)
      colnames(famdata)=colnames(dataset)
      famdata$network=as.factor(droplevels(famdata$network))
      famdata$nettype=as.factor(droplevels(famdata$nettype))
      # If there is only one good network:
      if(length(levels(famdata$network))==1){
        test1="glm"
        test2="none"
        nettype=levels(famdata$nettype)[1]
        scala=scale(famdata$distance)
        # More non-convergent family
        if(!family%in%c("lauraceae")){
          print_glm_outputs(famdata,family,nettype)
        }
      } else {
        # If we've only got one network type
        if(length(levels(famdata$nettype))==1){
          test1="glmer"
          test2="none"
          scala=scale(famdata$distance)
          nettype=levels(famdata$nettype)[1]
          print_glmer_notype_outputs(famdata,family,nettype)
        } else {
        # If we have both network types going on too...        
          pps=famdata[which(famdata$nettype=="pp"),]
          phs=famdata[which(famdata$nettype=="ph"),]  
          # What do we do with PP?  
          if(length(levels(as.factor(droplevels(as.factor(pps$network)))))>1){
              test1="glmer"
              print_glmer_notype_outputs(pps,family,"pp")
            } else {
              test1="glm"
              print_glm_outputs(pps,family,"pp")
            }
          if(length(levels(as.factor(droplevels(as.factor(phs$network)))))>1){            
              test2="glmer"
              print_glmer_notype_outputs(phs,family,"ph")
            } else {
              test2="glm"
              if(!family%in%c("sapindaceae")){
                print_glm_outputs(phs,family,"ph")
              } else {
                test2="reject_Sapindaceae"
              }
            }
          scala1=scale(pps$distance)
          # Can't add pp scales this
          # what_scale[i,1]=paste(family,"pp",sep='_')
          # what_scale[i,2]=attributes(scala1)$"scaled:center"
          # what_scale[i,3]=attributes(scala1)$"scaled:scale"

          i=i+1
          # PH values will be entered in the wrapper
          scala=scale(phs$distance)
          nettype="both"
        }
      }      
    } else {
      test1="reject"
      test2="reject"
      nettype="reject"
      scala=scale(dataset$distance)
    }
  }
  print(c(family,test1,test2,nettype))
  output=c(i,test1,test2,nettype,as.numeric(attributes(scala)$"scaled:center"),as.numeric(attributes(scala)$"scaled:scale"))
  return(output)
}

build_frankendata=function(families,frankendata){
  for(family in families){
  subdata=samefam[which(samefam$family==family),]
  # Check: can we fit this?
  tested=check_dataset(subdata)
  if(tested=='ok'){
  subdata$network=as.factor(droplevels(subdata$network))
  subdata$nettype=as.factor(droplevels(subdata$nettype))
  if(length(levels(subdata$network))==1){
    frankendata=rbind(frankendata,subdata)  
  } else {
    # Family in more than one network. 
    famdata=matrix(nrow=0,ncol=ncol(subdata))          # Make a dummy dataset to keep the good networks
    networks=levels(subdata$network)
    # Check whether each network has 2+ rows, keep only the good ones
    for(network in networks){
      netdata=subdata[which(subdata$network==network),] 
      tested=check_dataset(netdata)
      if(tested=="ok"){
        famdata=rbind(famdata,netdata)
      }
    }
    if(check_dataset(famdata)=="ok"){
      famdata=as.data.frame(famdata)
      colnames(famdata)=colnames(subdata)
      famdata$network=as.factor(droplevels(famdata$network))
      famdata$nettype=as.factor(droplevels(famdata$nettype))
      frankendata=rbind(frankendata,famdata)
    }
  }
  }
}
  return(frankendata)
}


# Now we're making progress! On to the pesky networks that don't fit right
families=levels(droplevels(samefam$family))
i=1
for(family in families){
  # print(family)
  subdata=samefam[which(samefam$family==family),]
  # Check: can we fit this?
  tested=check_dataset(subdata)

  if(tested=='ok'){
    params=select_model(subdata,family,i)
    i=as.numeric(params[1])
    test1=params[2]
    test2=params[3]
    nettype=params[4]
    center=as.numeric(params[5])
    scaler=as.numeric(params[6])
    # i=params[6]

    if(test2=="none"){
      if(test1=="glm"){
        which_test[i,1]=family
        which_test[i,2]="glm"
        which_test[i,3]=nettype
        # These guys have numerically 0/1 probabilities. Inspect by hand.
      } else {
        # Think I need to do this in the loop bc. famdata 
        which_test[i,1]=family
        which_test[i,2]="glmer_notype"
        which_test[i,3]=nettype
     }
    # # One scale for things with one network family
    what_scale[i,1]=family
    what_scale[i,2]=center
    what_scale[i,3]=scaler   
    } else {
    # Calling functions within selection for these fullas
      which_test[i,2]=test1
      which_test[i,1]=family
      which_test[i,3]="both_pp"
      i=i+1
      which_test[i,2]=test2
      which_test[i,1]=family
      which_test[i,3]="both_ph"
    # Two scales for things with two network families. Entering scales for PP in select_model
    what_scale[i,1]=paste(family,"ph",sep='_')
    what_scale[i,2]=center
    what_scale[i,3]=scaler
    }
  }
  i=i+1
} 


which_test=which_test[which(!is.na(which_test[,1])),]
write.table(which_test,file='../data/Jaccard/families_to_networks/which_test_for_each_family.tsv',sep='\t')

frankendata=build_frankendata(families,frankendata)
frankendata=as.data.frame(frankendata)
scala=scale(frankendata$distance)
what_scale[i,1]="overall"
what_scale[i,2]=attributes(scala)$"scaled:center"
what_scale[i,3]=attributes(scala)$"scaled:scale"

reg_unranked_scaled=glmer(cbind(n_shared_animals,n_notshared)~scale(distance)*nettype + (1+scale(distance)|network),data=frankendata,family="binomial")
write.table(ranef(reg_unranked_scaled)$network,file='../data/Jaccard/families_to_networks/within_family_random_effects_network.csv',sep=',')

what_scale=what_scale[which(!is.na(what_scale[,1])),]
write.table(what_scale,file='create_figures/scale_list.tsv',sep='\t')
#### frankendata caught 1606/64510 pairs, none of the overall slopes are significant over these fellas.

save.image('cladewise_data.Rdata')





