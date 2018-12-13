import csv
import sys
import os
import re


def extract_plant_names(filename,plant_names):

  f=open(filename,'r')
  filebase=csv.DictReader(f)

  for row in filebase:
    for key in row:
      if key not in ['','None',None]:
        plant_names.add((key,filename))
  f.close()

  return plant_names

def print_name_list(plant_names):
  outfile=open('../../data/plant_phylogeny/original_names.tsv','w')
  outfile.write('original_name\toriginal_genus\tweb\tshortened_name\n')
  for (item,web) in plant_names:
    webname=web.split('/')[-1]
    if '_' in item:
      splitname=item.split('_')
    else:
      splitname=item.split()
    if item=="Cuphea o'donellii": # Dat apostrophe though
      item="Cuphea odonellii"
      splitname=['Cuphea','odonellii']

    if len(splitname) in [1,2]: # Regular genus, species case or just genus. Nothing fancy.
      outfile.write(item+'\t'+splitname[0].capitalize()+'\t'+webname+'\t'+' '.join(splitname).capitalize()+'\n')
    elif 'var.' in splitname or 'subsp.' in splitname: # Don't care about subspecies, varieties.
      outfile.write(item+'\t'+splitname[0].capitalize()+'\t'+webname+'\t'+' '.join(splitname[:2]).capitalize()+'\n')
    elif 'PL' in splitname:  # Unknown numbered species with web IDs to ensure distinctness
      species=splitname[0].split()
      other=splitname[1:]
      webtag=species[-2]+'_'+species[-1]+''.join(other)
      outfile.write(item+'\t'+species[0]+'\t'+webname+'\t'+species[0].capitalize()+' '+webtag+'\n')
    elif 'Unknown' in splitname or 'Unidentified' in splitname or 'Other' in splitname:
      outfile.write(item+'\t'+splitname[0].capitalize()+'\t'+webname+'\t'+splitname[0]+' '+'_'.join(splitname[1:]).capitalize()+'\n')
    else:
      if 'sp.' in splitname or 'sp' in splitname:
        modname=[bit for bit in splitname if bit not in ['sp','sp.']]
        outfile.write(item+'\t'+splitname[0].capitalize()+'\t'+webname+'\t'+' '.join(modname).capitalize()+'\n')
      elif 'unidentified' in splitname or 'subgen.' in splitname:
        modname=[bit for bit in splitname if bit not in ['unidentified','subgen']]
        outfile.write(item+'\t'+splitname[0].capitalize()+'\t'+webname+'\t'+' '.join(modname).capitalize()+'\n')
      else:
        outfile.write(item+'\t'+splitname[0].capitalize()+'\t'+webname+'\t'+' '.join(splitname).capitalize()+'\n')

  outfile.close()


# Now we have a list of all the original species names to go into taxize.


def main():

  plant_names=set()

  for directory in ['../../data/Uncorrected_Matrices/Stouffer_Ecology_Matrices/','../../data/Uncorrected_Matrices/Plant_herbivore_matrices/']:
    print directory
    files=os.listdir(directory)

    for filename in files:
      if filename!='ph-peralta-2014-marlborough-metaweb.csv': # Only use the flipped version
        plant_names=extract_plant_names(directory+filename,plant_names)

  print_name_list(plant_names)
  print 'Feed the list of original names through taxize now'

if __name__ == '__main__':
  main()
