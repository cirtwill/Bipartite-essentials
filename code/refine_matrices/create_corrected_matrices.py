import csv
import sys
import os
import re

# Gymnosperms: PH (13 plants)
# Adding unmatched species manually using Mat's R code (bottom)
# Peralta has 11 of the unmatched.
# Coley has 1 unmatched, bodner has 3, bluthgen has 2
webs_with_unmatched=['ph-peralta-2014-marlborough-metaweb.new','ph_bluthgen_2006_borneo_handmade.new','ph_coley_2006_panama_handmade.new','ph_bodner_2010_handmade.new']

def create_name_dict(namefile):
  namedict={}
  f=open(namefile,'r')
  for line in f:
    if len(line.split('\t'))!=2:
      print line.split('\t')
      sys.exit()
    if line.split('\t')[0]!='Input':
      namedict[line.split('\t')[0]]=line.split('\t')[1].split('\n')[0]
  f.close()
  return namedict

def rowlist_builder(matfile,directory):
  g=open(directory+matfile,'r')
  rows=csv.DictReader(g)

  rowslist=[]
  for row in rows:
    rowslist.append(row)
  g.close()
  return rowslist

def slashdelim_builder(namedict,matfile,directory,slashdelims): # Also makes little phylogenies
  if 'M_PL' in matfile:
    filenum=int(matfile.split('_')[-1].split('.')[0])
  else:
    filenum=0
  rowslist=rowlist_builder(matfile,directory)
  for plant in rowslist[0].keys():
    if plant not in [None,"''",' ','']:
      if plant not in namedict.keys():
        print plant, matfile
        sys.exit()
      mscname=namedict[plant]
      modname='/'.join(mscname.split('/')[:2])+'/'+'_'.join(mscname.split('/')[1:])
      slashdelims.append(modname)        
  return slashdelims

def slashdelim_printer(slashdelims,phylofile): # Makes one enormous phylogeny
  if 'ph' not in phylofile:
    outfile=open('../../data/plant_phylogeny/PP_webs/'+phylofile.split('.csv')[0]+'_tree.tsv','w')
  else:
    outfile=open('../../data/plant_phylogeny/PH_webs/'+phylofile.split('.csv')[0]+'_tree.tsv','w')
  for slashline in slashdelims:
    if slashline!='':
      if slashline.split('\\')[0]!='':
        outfile.write(slashline+'\n')
  outfile.close()

  print phylofile, 'done'

def corrected_matrix_printer(matfile,directory,namedict,newdir):
  rowslist=rowlist_builder(matfile,directory)

  header=sorted(rowslist[0].keys())
  if None in header:
    header.remove(None)

  newheader=[]
  for plant in header:
    if plant!='':
      mscname=namedict[plant]
      modname='_'.join(mscname.split('/')[1:])
    else:
      modname=''
    newheader.append(modname)
  newmatrix=open(newdir+matfile.split('.csv')[0]+'_corrected.csv','w')
  newmatrix.write(','.join(newheader)+','+'\n')

  for row in rowslist:
    for key in header:
      newmatrix.write(row[key]+',')
    newmatrix.write('\n')
  newmatrix.close()

def main():

  namefile='../../data/plant_phylogeny/inputs_to_outputs.tsv'
  namedict=create_name_dict(namefile) # Dict of original key to output
  print 'name dict made'

  # Almost there. Poll tree still too big though - need to split.

  newdirectory='../../data/Corrected_Matrices/'
  olddirectory='../../data/Uncorrected_Matrices/'
  for tail in ['Stouffer_Ecology_Matrices/','Plant_herbivore_matrices/']:
    directory=olddirectory+tail
    newdir=newdirectory+tail
    files=os.listdir(directory)
    for matfile in sorted(files):
      slashdelims=[] # Making separate trees for each web now. Want to know how many plants need manual adding to each tree.
      if matfile not in ['ph-otte-1977-NorthAmerica-handmade.csv',  # North-America wide and not worth including
      'ph-peralta-2014-marlborough-metaweb.csv', 'ph-leather-1991-Finland.csv',  # The unflipped version (flipped is in)
      'ph-cagnolo-2011-Argentina-handmade.csv', 'ph-leather-1991-Britan.csv' ]:  # We don't want leaf-miners
        slashdelim_builder(namedict,matfile,directory,slashdelims)
        slashdelim_printer(slashdelims,matfile)

        # Still need to have a go at the corrected matrices.
        corrected_matrix_printer(matfile,directory,namedict,newdir)

  print 'matrices have been re-created with tipnames corresponding to phylogeny'

if __name__ == '__main__':
  main()


# Bluthgen
# library(phytools)
# tre<-read.tree('ph_bluthgen_2006_borneo_handmade.new')
# node<-grep('Spermatophyta',tre$node.label)+length(tre$tip.label)
# anc <- tre$edge[which(tre$edge[,2] == node),1]
# brlen <- nodeheight(tre, 1) - nodeheight(tre, anc)
# tip <- list(edge= matrix(c(2,1),1,2), tip.label='selaginella_sp170', edge.length=brlen, Nnode=1)
# class(tip) <- "phylo"
# tre <- bind.tree(tre,tip,where=anc)

# node<-grep('Eudicot',tre$node.label)+length(tre$tip.label)
# anc <- tre$edge[which(tre$edge[,2] == node),1]
# brlen <- nodeheight(tre, 1) - nodeheight(tre, anc)
# tip <- list(edge= matrix(c(2,1),1,2), tip.label='tetracera_indica', edge.length=brlen, Nnode=1)
# class(tip) <- "phylo"
# tre <- bind.tree(tre,tip,where=anc)

# write.tree(tre,'ph_bluthgen_2006_borneo_handmade.new')

# # Coley
# library(phytools)
# tre<-read.tree('ph_coley_2006_panama_handmade.new')
# node<-grep('Eudicot',tre$node.label)+length(tre$tip.label)
# anc <- tre$edge[which(tre$edge[,2] == node),1]
# brlen <- nodeheight(tre, 1) - nodeheight(tre, anc)
# tip <- list(edge= matrix(c(2,1),1,2), tip.label='doliocarpus_major', edge.length=brlen, Nnode=1)
# class(tip) <- "phylo"
# tre <- bind.tree(tre,tip,where=anc)
# write.tree(tre,'ph_coley_2006_panama_handmade.new')

# Can't have congeners be closer because no internal node.
# Maybe can install internal nodes, but will have to decide distances between congeners/confamilies. May be able to look these up?

# # Bodner (dennstaedtiaceae/pteridium/arachnoideum, gleicheniaceae/sticherus/sp137, dennstaedtiaceae/pteridium/sp112)
# Adding an internal node for Polypodiales at 357my (Testo and Sundue, 2016 via Angiosperm Phylogeny Website)
# library(phytools,treeman)
# tre<-read.tree('ph_bodner_2010_handmade.new')
# node<-grep('Spermatophyta',tre$node.label)+length(tre$tip.label)
# anc <- tre$edge[which(tre$edge[,2] == node),1]
# brlen <- nodeheight(tre, 1) - nodeheight(tre, anc)
# tip <- list(edge= matrix(c(2,1),1,2), tip.label='sticherus_sp137', edge.length=brlen, Nnode=1)
# class(tip) <- "phylo"
# tre <- bind.tree(tre,tip,where=anc)

# node<-grep('Spermatophyta',tre$node.label)+length(tre$tip.label)
# anc <- tre$edge[which(tre$edge[,2] == node),1]
# brlen <- nodeheight(tre, 1) - nodeheight(tre, anc)
# tip <- list(edge= matrix(c(2,1),1,2), tip.label='pteridium_arachnoideum', edge.length=brlen, Nnode=1)
# class(tip)<- "phylo"
# tre <- bind.tree(tre,tip,where=anc)

# node<-grep('Spermatophyta',tre$node.label)+length(tre$tip.label)
# anc <- tre$edge[which(tre$edge[,2] == node),1]
# brlen <- nodeheight(tre, 1) - nodeheight(tre, anc)
# tip <- list(edge= matrix(c(2,1),1,2), tip.label='pteridium_sp112', edge.length=brlen, Nnode=1)
# class(tip)<- "phylo"
# tre <- bind.tree(tre,tip,where=anc)
# write.tree(tre,'ph_bodner_2010_handmade.new')

# Peralta: 
# escalloniaceae/quintinia/serrata, # Angiosperm
# blechnaceae/blechnum/discolor,
# blechnaceae/blechnum/minus,
# cyatheaceae/cyathea/dealbata,
# cyatheaceae/cyathea/medullaris,
# dicksoniaceae/dicksonia/sp36,
# marattiaceae/marattia/salicina,

# library(phytools)
# tre<-read.tree("ph-peralta-2014-marlborough-metaweb.new")
# # Angiosperm
# node<-grep('Asterales',tre$node.label)+length(tre$tip.label)
# anc <- tre$edge[which(tre$edge[,2] == node),1]
# brlen <- nodeheight(tre, 1) - nodeheight(tre, anc)
# tip <- list(edge= matrix(c(2,1),1,2), tip.label='quintinia_serrata', edge.length=brlen, Nnode=1)
# class(tip) <- "phylo"
# tre <- bind.tree(tre,tip,where=anc)

# # Ferns and tree ferns
# node<-grep('Spermatophyta',tre$node.label)+length(tre$tip.label)
# anc <- tre$edge[which(tre$edge[,2] == node),1]
# brlen <- nodeheight(tre, 1) - nodeheight(tre, anc)
# tip <- list(edge= matrix(c(2,1),1,2), tip.label='blechnum_discolor', edge.length=brlen, Nnode=1)
# class(tip)<- "phylo"
# tre <- bind.tree(tre,tip,where=anc)
# node<-grep('Spermatophyta',tre$node.label)+length(tre$tip.label)
# anc <- tre$edge[which(tre$edge[,2] == node),1]
# brlen <- nodeheight(tre, 1) - nodeheight(tre, anc)
# tip <- list(edge= matrix(c(2,1),1,2), tip.label='blechnum_minus', edge.length=brlen, Nnode=1)
# class(tip)<- "phylo"
# tre <- bind.tree(tre,tip,where=anc)
# node<-grep('Spermatophyta',tre$node.label)+length(tre$tip.label)
# anc <- tre$edge[which(tre$edge[,2] == node),1]
# brlen <- nodeheight(tre, 1) - nodeheight(tre, anc)
# tip <- list(edge= matrix(c(2,1),1,2), tip.label='cyathea_dealbata', edge.length=brlen, Nnode=1)
# class(tip)<- "phylo"
# tre <- bind.tree(tre,tip,where=anc)
# node<-grep('Spermatophyta',tre$node.label)+length(tre$tip.label)
# anc <- tre$edge[which(tre$edge[,2] == node),1]
# brlen <- nodeheight(tre, 1) - nodeheight(tre, anc)
# tip <- list(edge= matrix(c(2,1),1,2), tip.label='cyathea_medullaris', edge.length=brlen, Nnode=1)
# class(tip)<- "phylo"
# tre <- bind.tree(tre,tip,where=anc)
# node<-grep('Spermatophyta',tre$node.label)+length(tre$tip.label)
# anc <- tre$edge[which(tre$edge[,2] == node),1]
# brlen <- nodeheight(tre, 1) - nodeheight(tre, anc)
# tip <- list(edge= matrix(c(2,1),1,2), tip.label='dicksonia_sp36', edge.length=brlen, Nnode=1)
# class(tip)<- "phylo"
# tre <- bind.tree(tre,tip,where=anc)
# node<-grep('Spermatophyta',tre$node.label)+length(tre$tip.label)
# anc <- tre$edge[which(tre$edge[,2] == node),1]
# brlen <- nodeheight(tre, 1) - nodeheight(tre, anc)
# tip <- list(edge= matrix(c(2,1),1,2), tip.label='marattia_salicina', edge.length=brlen, Nnode=1)
# class(tip)<- "phylo"
# tre <- bind.tree(tre,tip,where=anc)

# write.tree(tre,"ph-peralta-2014-marlborough-metaweb.new")

