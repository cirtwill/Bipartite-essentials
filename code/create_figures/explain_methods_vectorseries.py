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
from PyGrace.drawing_objects import DrawText, DrawLine, DrawBox
from PyGrace.axis import LINEAR_SCALE, LOGARITHMIC_SCALE

from PyGrace.Extensions.distribution import CDFGraph, PDFGraph
from PyGrace.Extensions.latex_string import LatexString, CONVERT
from PyGrace.Extensions.colorbar import SolidRectangle, ColorBar
from PyGrace.Styles.el import ElGraph, ElLinColorBar, ElLogColorBar

# The idea here is to use the interaction matrix for MPL033 to make a heat map like in the island project
# Just be aware that apparently the row names don't match the tip names?

def panel_a(graph): 

  intmatrix={
    "A":[1,1,1,0,1],
    "B":[0,1,1,1,0],
    "C":[1,1,0,1,0],
    "D":[1,1,0,1,0],
    "E":[1,0,0,0,0],
    "F":[1,0,0,0,0]
    }

  specieslist=["A","B","C","D","E","F"]

  datadict={}

  i=1
  j=6
  for species in specieslist:
    datadict[species]={}
    for value in intmatrix[species]:
      datadict[species][(i,j)]=value
      i=i+1
    j=j-1
    i=1

  return datadict


def vectorgrapher(grace,graph):
  xwidth=1
  ywidth=1

  names=["A","B","A","E","C","D","E","F"]
  polnames=[1,2,3,4,5]

  specials=graph.yaxis.tick.set_spec_ticks([12,11,9,8,6,5,3,2],[],tick_labels=names)
  # specials2=graph.xaxis.tick.set_spec_ticks([1,2,3,4,5],[],tick_labels=polnames)

  graph.world.xmax=9.5
  graph.world.ymax=12.5

  graph.world.xmin=0.5
  graph.world.ymin=0.5

  datadict=panel_a(graph)
  # graph.xaxis.tick.set_spec_ticks([],[])

  for species in ["A","B"]:
    for d in datadict[species]:
      graph.add_dataset([(d[0]-0.4*xwidth,d[1]-0.35*ywidth+6), (d[0]+0.4*xwidth,d[1]+0.35*ywidth+6)], SolidRectangle, 7*datadict[species][d])

  datadict["A"]={(5, 6): 0, (4, 6): 1, (3, 6): 1, (2, 6): 1, (1, 6): 1}
  for d in datadict["A"]:
    graph.add_dataset([(d[0]-0.4*xwidth,d[1]-0.35*ywidth+3), (d[0]+0.4*xwidth,d[1]+0.35*ywidth+3)], SolidRectangle, 7*datadict["A"][d])
  for d in datadict["E"]:
    graph.add_dataset([(d[0]-0.4*xwidth,d[1]-0.35*ywidth+6), (d[0]+0.4*xwidth,d[1]+0.35*ywidth+6)], SolidRectangle, 7*datadict["E"][d])    

  datadict["C"]={(5, 4): 0, (4, 4): 0, (3, 4): 1, (2, 4): 1, (1, 4): 1}
  datadict["D"]={(1, 3): 1, (2, 3): 1, (3, 3): 1, (4, 3): 0, (5, 3): 0}
  for species in ["C","D"]:
    for d in datadict[species]:
      graph.add_dataset([(d[0]-0.4*xwidth,d[1]-0.35*ywidth+2), (d[0]+0.4*xwidth,d[1]+0.35*ywidth+2)], SolidRectangle, 7*datadict[species][d])

  for species in ["E","F"]:
    for d in datadict[species]:
      graph.add_dataset([(d[0]-0.4*xwidth,d[1]-0.35*ywidth+1), (d[0]+0.4*xwidth,d[1]+0.35*ywidth+1)], SolidRectangle, 7*datadict[species][d])

  graph.add_drawing_object(DrawText,text='total',x=7,y=13,loctype='world',char_size=1.5,just=2)
  graph.add_drawing_object(DrawText,text='partial',x=8.25,y=13,loctype='world',char_size=1.5,just=2)
  graph.add_drawing_object(DrawText,text='none',x=9.5,y=13,loctype='world',char_size=1.5,just=2)
  graph.add_drawing_object(DrawText,text='distance',x=11.5,y=13,loctype='world',char_size=1.5,just=2)

  graph.add_drawing_object(DrawText,text='1',x=7,y=11,loctype='world',char_size=1.5,just=2)
  graph.add_drawing_object(DrawText,text='0',x=7,y=8,loctype='world',char_size=1.5,just=2)
  graph.add_drawing_object(DrawText,text='3',x=7,y=5,loctype='world',char_size=1.5,just=2)
  graph.add_drawing_object(DrawText,text='1',x=7,y=2,loctype='world',char_size=1.5,just=2)

  graph.add_drawing_object(DrawText,text='6',x=8.25,y=11,loctype='world',char_size=1.5,just=2)
  graph.add_drawing_object(DrawText,text='3',x=8.25,y=8,loctype='world',char_size=1.5,just=2)
  graph.add_drawing_object(DrawText,text='0',x=8.25,y=5,loctype='world',char_size=1.5,just=2)
  graph.add_drawing_object(DrawText,text='0',x=8.25,y=2,loctype='world',char_size=1.5,just=2)

  graph.add_drawing_object(DrawText,text='3',x=9.5,y=11,loctype='world',char_size=1.5,just=2)
  graph.add_drawing_object(DrawText,text='3',x=9.5,y=8,loctype='world',char_size=1.5,just=2)
  graph.add_drawing_object(DrawText,text='0',x=9.5,y=5,loctype='world',char_size=1.5,just=2)
  graph.add_drawing_object(DrawText,text='0',x=9.5,y=2,loctype='world',char_size=1.5,just=2)

  graph.add_drawing_object(DrawText,text='30 My',x=11.5,y=11,loctype='world',char_size=1.5,just=2)
  graph.add_drawing_object(DrawText,text='100 My',x=11.5,y=8,loctype='world',char_size=1.5,just=2)
  graph.add_drawing_object(DrawText,text='10 My',x=11.5,y=5,loctype='world',char_size=1.5,just=2)
  graph.add_drawing_object(DrawText,text='50 My',x=11.5,y=2,loctype='world',char_size=1.5,just=2)


  graph.xaxis.tick.configure(major=1,minor_size=0,major_size=0)
  graph.yaxis.tick.configure(major=1,minor_size=0,major_size=0)

  graph.yaxis.ticklabel.configure(char_size=0)
  graph.xaxis.ticklabel.configure(char_size=0,place='opposite')

  graph.yaxis.tick.configure(major=1,minor_ticks=1,minor_grid='off')
  graph.xaxis.tick.configure(major=1,minor_ticks=1,minor_grid='off')

  graph.frame.configure(linewidth=0,color=0)
  graph.xaxis.bar.linewidth=0
  graph.yaxis.bar.linewidth=0

  graph.panel_label.configure(char_size=0,placement='oul',dy=.03,dx=.04) 

  return graph

def vectorgrapher1(grace,graph):
  xwidth=1
  ywidth=1

  names=["A","B","A","E","C","D","E","F"]
  polnames=[1,2,3,4,5]

  specials=graph.yaxis.tick.set_spec_ticks([12,11,9,8,6,5,3,2],[],tick_labels=names)
  # specials2=graph.xaxis.tick.set_spec_ticks([1,2,3,4,5],[],tick_labels=polnames)

  graph.world.xmax=9.5
  graph.world.ymax=7.5

  graph.world.xmin=0.5
  graph.world.ymin=0.5

  datadict=panel_a(graph)
  # graph.xaxis.tick.set_spec_ticks([],[])

  for species in ["A","B"]:
    for d in datadict[species]:
      print d
      graph.add_dataset([(d[0]-0.4*xwidth,d[1]-0.35*ywidth), (d[0]+0.4*xwidth,d[1]+0.35*ywidth)], SolidRectangle, 7*datadict[species][d])

  graph.add_drawing_object(DrawText,text='total',x=7,y=7,loctype='world',char_size=1.5,just=2)
  graph.add_drawing_object(DrawText,text='partial',x=8.25,y=7,loctype='world',char_size=1.5,just=2)
  graph.add_drawing_object(DrawText,text='none',x=9.5,y=7,loctype='world',char_size=1.5,just=2)
  graph.add_drawing_object(DrawText,text='distance',x=11.5,y=7,loctype='world',char_size=1.5,just=2)

  graph.add_drawing_object(DrawText,text='1',x=7,y=5,loctype='world',char_size=1.5,just=2)
  graph.add_drawing_object(DrawText,text='6',x=8.25,y=5,loctype='world',char_size=1.5,just=2)
  graph.add_drawing_object(DrawText,text='3',x=9.5,y=5,loctype='world',char_size=1.5,just=2)

  graph.add_drawing_object(DrawText,text='30 My',x=11.5,y=5,loctype='world',char_size=1.5,just=2)


  graph.xaxis.tick.configure(major=1,minor_size=0,major_size=0)
  graph.yaxis.tick.configure(major=1,minor_size=0,major_size=0)

  graph.yaxis.ticklabel.configure(char_size=0)
  graph.xaxis.ticklabel.configure(char_size=0,place='opposite')

  graph.yaxis.tick.configure(major=1,minor_ticks=1,minor_grid='off')
  graph.xaxis.tick.configure(major=1,minor_ticks=1,minor_grid='off')

  graph.frame.configure(linewidth=0,color=0)
  graph.xaxis.bar.linewidth=0
  graph.yaxis.bar.linewidth=0

  graph.panel_label.configure(char_size=0,placement='oul',dy=.03,dx=.04) 

  return graph

def vectorgrapher2(grace,graph):
  xwidth=1
  ywidth=1

  names=["A","B","A","E","C","D","E","F"]
  polnames=[1,2,3,4,5]

  specials=graph.yaxis.tick.set_spec_ticks([12,11,9,8,6,5,3,2],[],tick_labels=names)
  # specials2=graph.xaxis.tick.set_spec_ticks([1,2,3,4,5],[],tick_labels=polnames)

  graph.world.xmax=9.5
  graph.world.ymax=7.5

  graph.world.xmin=0.5
  graph.world.ymin=0.5

  datadict=panel_a(graph)
  # graph.xaxis.tick.set_spec_ticks([],[])

  datadict["C"]={(5, 4): 0, (4, 4): 0, (3, 4): 1, (2, 4): 1, (1, 4): 1}
  datadict["D"]={(1, 3): 1, (2, 3): 1, (3, 3): 1, (4, 3): 0, (5, 3): 0}
  for species in ["C","D"]:
    for d in datadict[species]:
      graph.add_dataset([(d[0]-0.4*xwidth,d[1]-0.35*ywidth+2), (d[0]+0.4*xwidth,d[1]+0.35*ywidth+2)], SolidRectangle, 7*datadict[species][d])

  for species in ["E","F"]:
    for d in datadict[species]:
      graph.add_dataset([(d[0]-0.4*xwidth,d[1]-0.35*ywidth+1), (d[0]+0.4*xwidth,d[1]+0.35*ywidth+1)], SolidRectangle, 7*datadict[species][d])

  graph.add_drawing_object(DrawText,text='total',x=7,y=7,loctype='world',char_size=1.5,just=2)
  graph.add_drawing_object(DrawText,text='partial',x=8.25,y=7,loctype='world',char_size=1.5,just=2)
  graph.add_drawing_object(DrawText,text='none',x=9.5,y=7,loctype='world',char_size=1.5,just=2)
  graph.add_drawing_object(DrawText,text='distance',x=11.5,y=7,loctype='world',char_size=1.5,just=2)

  graph.add_drawing_object(DrawText,text='3',x=7,y=5,loctype='world',char_size=1.5,just=2)
  graph.add_drawing_object(DrawText,text='1',x=7,y=2,loctype='world',char_size=1.5,just=2)

  graph.add_drawing_object(DrawText,text='0',x=8.25,y=5,loctype='world',char_size=1.5,just=2)
  graph.add_drawing_object(DrawText,text='0',x=8.25,y=2,loctype='world',char_size=1.5,just=2)

  graph.add_drawing_object(DrawText,text='0',x=9.5,y=5,loctype='world',char_size=1.5,just=2)
  graph.add_drawing_object(DrawText,text='0',x=9.5,y=2,loctype='world',char_size=1.5,just=2)

  graph.add_drawing_object(DrawText,text='10 My',x=11.5,y=5,loctype='world',char_size=1.5,just=2)
  graph.add_drawing_object(DrawText,text='50 My',x=11.5,y=2,loctype='world',char_size=1.5,just=2)
  
  graph.add_drawing_object(DrawText,text="Jaccard",x=5.75,y=7,loctype='world',char_size=1.5,just=2,color=10)
  graph.add_drawing_object(DrawText,text="1",x=5.75,y=5,loctype='world',char_size=1.5,just=2,color=10)
  graph.add_drawing_object(DrawText,text="1",x=5.75,y=2,loctype='world',char_size=1.5,just=2,color=10)

  graph.xaxis.tick.configure(major=1,minor_size=0,major_size=0)
  graph.yaxis.tick.configure(major=1,minor_size=0,major_size=0)

  graph.yaxis.ticklabel.configure(char_size=0)
  graph.xaxis.ticklabel.configure(char_size=0,place='opposite')

  graph.yaxis.tick.configure(major=1,minor_ticks=1,minor_grid='off')
  graph.xaxis.tick.configure(major=1,minor_ticks=1,minor_grid='off')

  graph.frame.configure(linewidth=0,color=0)
  graph.xaxis.bar.linewidth=0
  graph.yaxis.bar.linewidth=0

  graph.panel_label.configure(char_size=0,placement='oul',dy=.03,dx=.04) 

  return graph

def vectorgrapher3(grace,graph):
  xwidth=1
  ywidth=1

  names=["A","B","A","E","C","D","E","F"]
  polnames=[1,2,3,4,5]

  specials=graph.yaxis.tick.set_spec_ticks([12,11,9,8,6,5,3,2],[],tick_labels=names)
  # specials2=graph.xaxis.tick.set_spec_ticks([1,2,3,4,5],[],tick_labels=polnames)

  graph.world.xmax=9.5
  graph.world.ymax=7.5

  graph.world.xmin=0.5
  graph.world.ymin=0.5

  datadict=panel_a(graph)
  # graph.xaxis.tick.set_spec_ticks([],[])
  datadict["A"]={(5, 6): 0, (4, 6): 1, (3, 6): 1, (2, 6): 1, (1, 6): 1}
  for d in datadict["A"]:
    graph.add_dataset([(d[0]-0.4*xwidth,d[1]-0.35*ywidth), (d[0]+0.4*xwidth,d[1]+0.35*ywidth)], SolidRectangle, 7*datadict["A"][d])
  for d in datadict["E"]:
    graph.add_dataset([(d[0]-0.4*xwidth,d[1]-0.35*ywidth+3), (d[0]+0.4*xwidth,d[1]+0.35*ywidth+3)], SolidRectangle, 7*datadict["E"][d])    

  graph.add_drawing_object(DrawText,text='total',x=7,y=7,loctype='world',char_size=1.5,just=2)
  graph.add_drawing_object(DrawText,text='partial',x=8.25,y=7,loctype='world',char_size=1.5,just=2)
  graph.add_drawing_object(DrawText,text='none',x=9.5,y=7,loctype='world',char_size=1.5,just=2)
  graph.add_drawing_object(DrawText,text='distance',x=11.5,y=7,loctype='world',char_size=1.5,just=2)

  graph.add_drawing_object(DrawText,text='0',x=7,y=5,loctype='world',char_size=1.5,just=2)
  graph.add_drawing_object(DrawText,text='3',x=8.25,y=5,loctype='world',char_size=1.5,just=2)
  graph.add_drawing_object(DrawText,text='3',x=9.5,y=5,loctype='world',char_size=1.5,just=2)

  graph.add_drawing_object(DrawText,text='100 My',x=11.5,y=5,loctype='world',char_size=1.5,just=2)

  graph.add_drawing_object(DrawText,text="Jaccard",x=5.75,y=7,loctype='world',char_size=1.5,just=2,color=10)
  graph.add_drawing_object(DrawText,text="0.25",x=5.75,y=5,loctype='world',char_size=1.5,just=2,color=10)

  graph.xaxis.tick.configure(major=1,minor_size=0,major_size=0)
  graph.yaxis.tick.configure(major=1,minor_size=0,major_size=0)

  graph.yaxis.ticklabel.configure(char_size=0)
  graph.xaxis.ticklabel.configure(char_size=0,place='opposite')

  graph.yaxis.tick.configure(major=1,minor_ticks=1,minor_grid='off')
  graph.xaxis.tick.configure(major=1,minor_ticks=1,minor_grid='off')

  graph.frame.configure(linewidth=0,color=0)
  graph.xaxis.bar.linewidth=0
  graph.yaxis.bar.linewidth=0

  graph.panel_label.configure(char_size=0,placement='oul',dy=.03,dx=.04) 

  return graph

def main():

  colors=ColorBrewerScheme('Purples')
  colors.add_color(200,0,0,"Red")

  grace=Grace(colors=colors)
 
  graph1=grace.add_graph(Panel)

  vectorgrapher(grace,graph1)
  grace.write_file('../../manuscript/Figures/Sketches/methods_breakdown_manyvectors.eps')

  grace=MultiPanelGrace(colors=colors)
 
  graph1=grace.add_graph(Panel)

  grace.multi(rows=1,cols=1,width_to_height_ratio=2.2/1)

  vectorgrapher1(grace,graph1)
  grace.write_file('../../manuscript/Figures/Sketches/methods_breakdown_example.eps')

  grace=MultiPanelGrace(colors=colors)
 
  graph1=grace.add_graph(Panel)

  grace.multi(rows=1,cols=1,width_to_height_ratio=2.2/1)

  vectorgrapher3(grace,graph1)
  grace.write_file('../../manuscript/Figures/Sketches/methods_breakdown_nestedness.eps')

  grace=MultiPanelGrace(colors=colors)
 
  graph1=grace.add_graph(Panel)

  grace.multi(rows=1,cols=1,width_to_height_ratio=2.2/1)

  vectorgrapher2(grace,graph1)
  grace.write_file('../../manuscript/Figures/Sketches/methods_breakdown_weighting.eps')
if __name__ == '__main__':
  main()
