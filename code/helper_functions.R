make_numeric_matrix <- function(network_matrix){

  if('X'%in%colnames(network_matrix)){          # Trim any superfluous columns
    network_matrix$X=NULL    }
  if('X.1'%in%colnames(network_matrix)){          
    network_matrix$X.1=NULL    }

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


	return(numeric_matrix)
}


calculate_overlap <- function(numeric_matrix,plantpair){

	subnetwork=t(numeric_matrix[,plantpair,drop=FALSE])                 # select just the columns of interest
	subnetwork=subnetwork[,which(colSums(subnetwork)>0),drop=FALSE]     # get rid of animals that don't have interactions
	if(ncol(subnetwork) > 0){                                           # make sure there are at least some animals left
	  intersection=length(which(colSums(subnetwork)==2))      
	  union=ncol(subnetwork)
	  notshared=length(which(colSums(subnetwork)==1))
	  } else {
	  	intersection=0
	  	union=0
	  	notshared=0
	  }

	result=c(intersection,union,notshared)
	return(result)
}

