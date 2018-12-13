library(taxize)

data=read.table('../../data/plant_phylogeny/original_names.tsv',row.names=NULL,sep='\t')
colnames(data)=c("original_name","original_genus","web","shortened_name")
data<-data[2:nrow(data),]
for (c in 1:ncol(data)){
  data[,c]=as.character(data[,c])
  print(str(data[,c]))
}

data<-data[order(data$shortened_name),]
data$new_name<-NA
data$source<-NA
rownames(data)=paste0(data$original_name,data$web)

names=levels(as.factor(data$shortened_name))
n_unique=length(names) #2259 unique species

dumb_names=c("Arthropod parts", "Unidentified sp.", "Unidentified sp13_MPL040",
      "Unidentified sp14_MPL040", "Unidentified sp15_MPL040", "Unidentified sp16_MPL040",
      "Unidentified sp17_MPL040", "Unidentified sp18_MPL040", "Unidentified sp19_MPL040",
      "Unidentified sp20_MPL040", "Unidentified sp21_MPL040",  "Unidentified sp21_MPL041", 
      "Unidentified sp22_MPL040", "Unidentified sp23_MPL040", "Unidentified sp27_MPL046",
      "Unknown", "Unknown Forb_a", "Unknown Forb_b", "Unknown Forb_c", 
      "Unknown Forb_d","Unknown Forb_e","Unknown Forb_f",                
      "Unknown Forb_g","Unknown Forb_h","Unknown Forb_i",                
      "Unknown Forb_j","Unknown Forb_k","Unknown Forb_l",                
      "Unknown Forb_m","Unknown Forb_n","Unknown Forb_o",                
      "Unknown Forb_p","Unknown Forb_q","Unknown Forb_r",                
      "Unknown Forb_s","Unknown Voucher_no._1","Unknown lichen",
      "Unidentified Voucher_no.28",
      "Phasuba","Ceballosia fruticosa","Dalea spp.1","Dalea spp.2","Tyttnera scabra")

daleas=c("Dalea spp.1","Dalea spp.2")
# Dalea is ok but the spp. throws TNRS off

good_names=names[!names %in% dumb_names]
n_good=length(good_names)

# Note: tnrs does NOT preserve order of query lists. Fun.
mini=matrix(nrow=n_good,ncol=3)
colnames(mini)=c("orig_names","subnames","newnames")
mini[,1]=good_names
unique_tnrs_1=tnrs(query=mini[1:1000,1],getpost="POST",source="iPlant_TNRS")
mini[1:1000,2]=unique_tnrs_1$submittedname 
mini[1:1000,3]=unique_tnrs_1$matchedname 

unique_tnrs_2=tnrs(query=mini[1001:2000,1],getpost="POST",source="iPlant_TNRS")
mini[1001:2000,2]=unique_tnrs_2$submittedname
mini[1001:2000,3]=unique_tnrs_2$matchedname
unique_tnrs_3=tnrs(query=mini[2001:n_good,1],getpost="POST",source="iPlant_TNRS")
mini[2001:n_good,2]=unique_tnrs_3$submittedname
mini[2001:n_good,3]=unique_tnrs_3$matchedname
rownames(mini)=mini[,2] # Gotta use the sub names that come with the matched names

# Add the simple names back to data
for(r in 1:nrow(data)){
  key=data$shortened_name[r]
  if(key %in% good_names){
    data$new_name[r]=mini[key,2]
    data$source[r]="TNRS"
  } else {
    if(key %in% daleas){
      data$new_name[r]="Dalea"
      data$source[r]="TNRS_man"
    } else {
      data$new_name[r]="None"
      data$source[r]="manual"
    }
  }
}

data$class=NA
data$order=NA
data$family=NA
data$genus=NA
data$species=NA

for(r in 1:nrow(data)){
  if(data$source[r]=="manual"){
    data$class[r]="None"
    data$order[r]="None"
    data$family[r]="None"
    data$genus[r]="None"
    data$species[r]="None"
  } else {
    rowname=data$new_name[r]
    famjam=tax_name(query=rowname,get=c("class","order",
      "family","genus","species"),db="itis")
      data[r,]$class=famjam$class
      data[r,]$order=famjam$order
      data[r,]$family=famjam$family
      data[r,]$genus=famjam$genus
      data[r,]$species=famjam$species
  }
}




remainder=subset(splist,is.na(splist$new_names)) # That's all, folks!

# This tends to need re-launching several times...
# for(rowname in rownames(splist)[2120:2129]){
for(rowname in rownames(splist)){
  if(splist[rowname,]$new_names %in% c("unidentified","")){
    splist[rowname,]$class="unidentified"
    splist[rowname,]$order="unidentified"
    splist[rowname,]$superfamily="unidentified"
    splist[rowname,]$family="unidentified"
    splist[rowname,]$tribe="unidentified"
    splist[rowname,]$genus="unidentified"
    splist[rowname,]$species="unidentified"
    } else {
  # Even though it will slow everything down, saving in the middle of the loop should help when dealing with server bails
  save.image('taxize_corrections_bluthgen.Rdata')
  #trying itis first
  famjam=tax_name(query=splist[rowname,]$new_names,get=c("class","order","superfamily",
      "family","tribe","genus","species"),db="itis")
  splist[rowname,]$class=famjam$class
  splist[rowname,]$order=famjam$order
  splist[rowname,]$superfamily=famjam$superfamily
  splist[rowname,]$family=famjam$family
  splist[rowname,]$tribe=famjam$tribe
  splist[rowname,]$genus=famjam$genus
  splist[rowname,]$species=famjam$species
=======
medi=matrix(nrow=nrow(mini),ncol=6)
colnames(medi)=c("acceptedname","class","order","family","genus","species")
medi[,1]=mini[,3]
# First attempt with itis
for(r in 1:nrow(medi)){
# for(r in 2081:nrow(medi)){
  # if(!is.na(medi[r,5])){
  famjam=tax_name(query=medi[r,1],get=c("class","order","family","genus","species"),db="itis")
  if("class" %in% colnames(famjam)){
    medi[r,2]=famjam$class
  }
  if("order" %in% colnames(famjam)){
    medi[r,3]=famjam$order
  }
  if("family" %in% colnames(famjam)){
    medi[r,4]=famjam$family
  }
  if("genus" %in% colnames(famjam)){
    medi[r,5]=famjam$genus
  }
  if("species" %in% colnames(famjam)){
    medi[r,6]=famjam$species
  }
}#}


# Try NCBI on the stragglers
for(r in 1:nrow(medi)){
# for(r in 2081:nrow(medi)){
  if(!is.na(medi[r,2])){
  famjam=tax_name(query=medi[r,1],get=c("class","order","family","genus","species"),db="ncbi")
  if("class" %in% colnames(famjam)){
    medi[r,2]=famjam$class
  }
  if("order" %in% colnames(famjam)){
    medi[r,3]=famjam$order
  }
  if("family" %in% colnames(famjam)){
    medi[r,4]=famjam$family
  }
  if("genus" %in% colnames(famjam)){
    medi[r,5]=famjam$genus
  }
  if("species" %in% colnames(famjam)){
    medi[r,6]=famjam$species
  }
}}

# Still about half didn't work
for(r in 1:nrow(medi)){
  fullname=medi[r,1]
  genus=strsplit(fullname,' ')$acceptedname[1]
# for(r in 2081:nrow(medi)){
  if(!is.na(medi[r,6])){
  famjam=tax_name(query=genus,get=c("class","order","family","genus"),db="ncbi")
  if("class" %in% colnames(famjam)){
    medi[r,2]=famjam$class
>>>>>>> 6c7acd9b70749bfc546b51c5165cfa3347472ea0
  }
  if("order" %in% colnames(famjam)){
    medi[r,3]=famjam$order
  }
  if("family" %in% colnames(famjam)){
    medi[r,4]=famjam$family
  }
  if("genus" %in% colnames(famjam)){
    medi[r,5]=famjam$genus
  }
  medi[r,6]=fullname
}}

# And let's try itis too
for(r in 1:nrow(medi)){
  fullname=medi[r,1]
  genus=strsplit(fullname,' ')[[1]][1]
  print(genus)
# for(r in 2081:nrow(medi)){
  if(!is.na(medi[r,6])){
  famjam=tax_name(query=genus,get=c("class","order","family"),db="itis")
  if("class" %in% colnames(famjam)){
    medi[r,2]=famjam$class
  }
  if("order" %in% colnames(famjam)){
    medi[r,3]=famjam$order
  }
  if("family" %in% colnames(famjam)){
    medi[r,4]=famjam$family
  }
  medi[r,5]=famjam$genus
  medi[r,6]=fullname
}}

# Still >1000 that didn't work?!? 
dregs=medi[which(is.na(medi[,6])),]  
for(r in 1:nrow(dregs)){
  fullname=medi[r,1]
  genus=strsplit(fullname,' ')[[1]][1]
  dregs[r,5]=genus
}
for(gen in levels(as.factor(dregs[,5]))){
  famjam=tax_name(query=gen,get=c("class","order","family"),db="itis")
  for(r in 1:nrow(dregs)){
    if(dregs[r,5]==gen){
      if("class" %in% colnames(famjam)){
        dregs[r,2]=famjam$class
      }
      if("order" %in% colnames(famjam)){
        dregs[r,3]=famjam$order
      }
      if("family" %in% colnames(famjam)){
        dregs[r,4]=famjam$family
      }
    }
}}





write.table(splist, file='../../data/plant_phylogeny/corrected_names_bluthgen.tsv',sep=',')

