import sys
import os
import re
import random
from decimal import *
import math

from PyGrace.grace import Grace
from PyGrace.colors import RandomColorScheme, MarkovChainColorScheme, ColorBrewerScheme
from PyGrace.dataset import SYMBOLS
from PyGrace.Extensions.panel import Panel,MultiPanelGrace
from PyGrace.drawing_objects import DrawText, DrawLine
from PyGrace.axis import LINEAR_SCALE, LOGARITHMIC_SCALE

from PyGrace.Extensions.distribution import CDFGraph, PDFGraph
from PyGrace.Extensions.latex_string import LatexString, CONVERT
from PyGrace.Extensions.colorbar import SolidRectangle, ColorBar
from PyGrace.Styles.el import ElGraph, ElLinColorBar, ElLogColorBar

# The idea here is to use the interaction matrix for MPL033 to make a heat map like in the island project
# Just be aware that apparently the row names don't match the tip names?

def panel_a(graph): 

  intmatrix={
    "smilacina_trifolia_m_pl_033.csv":[0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0],
    "aronia_melanocarpa_m_pl_033.csv":[0,1,0,1,1,1,0,0,1,0,0,1,0,1,1,1,1,0,0,1,0,1,0,1,0,1,0,1,0,1,0],
    "spiraea_alba_m_pl_033.csv":[0,0,1,0,0,1,0,0,1,0,1,0,0,1,0,1,1,0,1,0,0,0,0,0,1,0,0,0,1,1,1],
    "kalmia_polifolia_m_pl_033.csv":[0,1,0,0,1,1,1,1,1,1,1,0,1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
    "andromeda_glaucophylla_m_pl_033.csv":[0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "gaylussacia_baccata_m_pl_033.csv":[0,1,1,0,1,1,1,0,1,1,1,0,1,0,1,0,1,1,0,0,1,0,0,0,0,0,0,1,0,0,0],
    "kalmia_angustifolia_m_pl_033.csv":[0,0,0,0,0,1,0,1,1,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0],
    "ledum_groenlandicum_m_pl_033.csv":[0,1,1,1,1,1,0,1,1,1,1,0,0,0,1,0,1,1,0,1,0,0,0,0,0,1,1,1,1,1,0],
    "chamaedaphne_calyculata_m_pl_033.csv":[0,1,0,1,1,1,1,1,1,0,1,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,1,0,0,0],
    "vaccinium_myrtilloides_m_pl_033.csv":[0,1,1,1,1,1,1,1,1,1,1,0,1,1,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0],
    "nemopanthus_mucronatus_m_pl_033.csv":[1,1,0,0,1,1,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,1,0,1,1,0,1,0,0]  }

  specieslist=["smilacina_trifolia_m_pl_033.csv","aronia_melanocarpa_m_pl_033.csv","spiraea_alba_m_pl_033.csv",
    "kalmia_polifolia_m_pl_033.csv","andromeda_glaucophylla_m_pl_033.csv","gaylussacia_baccata_m_pl_033.csv",
    "kalmia_angustifolia_m_pl_033.csv","ledum_groenlandicum_m_pl_033.csv","chamaedaphne_calyculata_m_pl_033.csv",
    "vaccinium_myrtilloides_m_pl_033.csv","nemopanthus_mucronatus_m_pl_033.csv"]

  datadict={}

  i=1
  j=11
  for species in specieslist:
    datadict[species]={}
    for value in intmatrix[species]:
      datadict[species][(i,j)]=value
      i=i+1
    j=j-1
    i=1

  return datadict

def grapher():
  grace=Grace(colors=ColorBrewerScheme('Purples'))

  xwidth=1
  ywidth=1

  graph=grace.add_graph()

  names=["Smilacina trifolia","Aronia melanocarpa","Spiraea alba",
    "Kalmia polifolia","Andromeda glaucophylla","Gaylussacia baccata",
    "Kalmia angustifolia","Ledum groenlandicum","Chamaedaphne calyculata",
    "Vaccinium myrtilloides","Nemopanthus mucronatus"]


  specials=graph.yaxis.tick.set_spec_ticks([11,10,9,8,7,6,5,4,3,2,1],[],tick_labels=names)

  graph.world.xmax=31.5
  graph.world.ymax=11.5

  graph.world.xmin=0.5
  graph.world.ymin=0.5

  datadict=panel_a(graph)
  graph.xaxis.tick.set_spec_ticks([],[])

  for species in datadict:
    for d in datadict[species]:
      graph.add_dataset([(d[0]-0.5*xwidth,d[1]-0.5*ywidth), (d[0]+0.5*xwidth,d[1]+0.5*ywidth)], SolidRectangle, 7*datadict[species][d])

  graph.xaxis.tick.configure(major=1,minor_size=0,major_size=0)
  graph.yaxis.tick.configure(major=1,minor_size=0,major_size=0)

  graph.yaxis.ticklabel.configure(char_size=.75)
  graph.xaxis.ticklabel.configure(char_size=.5)

  graph.yaxis.tick.configure(major=1,minor_ticks=1,minor_grid='on',minor_linewidth=2)
  graph.xaxis.tick.configure(major=1,minor_ticks=1,minor_grid='on')


  graph.frame.linewidth=1
  graph.xaxis.bar.linewidth=1
  graph.yaxis.bar.linewidth=1


  # Adding gridlines
  for x in range(0,12):
    hline=graph.add_drawing_object(DrawLine,start=(.5,.5+x),end=(31.5,.5+x),loctype='world',color=1,linewidth=1,linestyle=2)
  for x in range(0,32):
    vline=graph.add_drawing_object(DrawLine,start=(.5+x,.5),end=(.5+x,11.5),loctype='world',color=1,linewidth=1,linestyle=2)


  grace.write_file('../../talk/talkfigs/R/interaction_matrix_MPL033.eps')

def main():

  grapher()

if __name__ == '__main__':
  main()
