import csv
import sys
import os
import re

### known genera/species of plants and insects to confirm orientation of matrices

common_bugs=set(['Apis','Bombus','Culex','Papilio','Xylocopa','Ichneumonidae',
                'Acarina','Peremptor','Aedes', 'Xanthia','Abraxas','Melanopus',
                'Bootettix','Phalera','Gomphocerus','Opeia','Melanoplus','Diptera',
                'Cleora.sp','Holocola.sp','Neolepta_34','Acacus_sarawacus','Bryoptera',
                'Udranomia_sp','CURC012'])

common_plants=set(['Artemisia','Carolus','Quercus','Avicenna','Lantana',
                    'Opuntia','Epilobium','Vaccinium','Cassinia','Pedicularis',
                    'Prunus','Aristida','Erigonum','Bromus','Lotus','Mentha','Acaena',
                    'Oxalis','Astragalus','Passiflora','Adenocarpus','Asclepias','Thymus',
                    'Viola','Trillium','Mimosa','Claytonia','Myrteola','Angelica','Allium','Ribes',
                    'coprosma_robusta','Cordia_dichotoma','Liana_unidentified','Hyptis_sp',
                    'Cordia_bicolor','Ficus_copiosa'
                    ])

def are_plants_columns(filename,inverted_matrices):
  row_genera=set()
  column_genera=set()

  f=open(filename,'r')
  filebase=csv.DictReader(f)

  for row in filebase:
    for key in row:
      if key=='':
        row_genera.add(row[key].split(' ')[0])
      else:
        column_genera.add(str(key).split(' ')[0])

  f.close()
  # print row_genera
  if column_genera&common_bugs!=set([]):
    print 'It appears that file ', filename, ' has pollinators as columns'
    inverted_matrices.append(filename)

    if row_genera&common_plants!=set([]):
      print 'Indeed, plants are on the rows.' 

  else:

    if row_genera&common_bugs==set([]):
      print 'Add more insects', filename
    if column_genera&common_plants==set([]):
      print 'Add more plants', filename


def flip_the_matrix(matfile):
  f=open(matfile,'r')
  filebase=csv.DictReader(f)

  reversedict={}

  plantnames=set()

  for row in filebase:
    plantname=row['']
    plantnames.add(plantname)
    for animal in row.keys():
      if animal!='':
        try:
          reversedict[animal][plantname]=row[animal]
        except KeyError:
          reversedict[animal]={plantname:row[animal]}

  f.close()
  plantnames=sorted(plantnames)

  newmat=open(matfile+'.flipped','w')
  newmat.write(''+','+','.join(plantnames)+'\n')
  for plant in reversedict:
    newmat.write(plant)
    for animal in reversedict[plant]:
      newmat.write(','+str(reversedict[plant][animal]))
    newmat.write('\n')
  newmat.close()

  print matfile + ' has been flipped'



def main():

  for directory in ['../../data/Uncorrected_Matrices/Stouffer_Ecology_Matrices/',
                    '../../data/Uncorrected_Matrices/Plant_herbivore_matrices/']:

    inverted_matrices=[]

    files=os.listdir(directory)
    # files=files[1:2]

    for filename in files:
      are_plants_columns(directory+filename,inverted_matrices)

    if inverted_matrices==[]:
      print 'All the matrices in ', directory, ' are sensibly ordered'
    else:
      # print inverted_matrices
      for matfile in inverted_matrices:
        flip_the_matrix(matfile)
        
      inverted_matrices_2=[]
      for filename in files:
        if directory+filename not in inverted_matrices:
          are_plants_columns(directory+filename,inverted_matrices)

      if inverted_matrices_2==inverted_matrices:
        print 'All the matrices in ', directory, ' are sensibly ordered'
      else:
        if inverted_matrices_2!=[]:
          print 'Some matrices have not been flipped: '
          print inverted_matrices_2
          for matfile in inverted_matrices_2:
            flip_the_matrix(matfile)

if __name__ == '__main__':
  main()
