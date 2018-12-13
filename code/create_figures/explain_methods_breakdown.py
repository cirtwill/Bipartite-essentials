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

def quaddict_maker(quad):
  specieslist=["A","B"]

  datadict={}

  i=1
  j=7
  for species in specieslist:
    datadict[species]={}
    for value in quad[species]:
      datadict[species][(i,j)]=value
      i=i+1
    j=j-1
    i=1

  return datadict

def grapher(grace,graph):
  xwidth=1
  ywidth=1

  names=["A","B","C","D","E","F"]
  polnames=[1,2,3,4,5]

  specials=graph.yaxis.tick.set_spec_ticks([6,5,4,3,2,1],[],tick_labels=names)
  specials2=graph.xaxis.tick.set_spec_ticks([1,2,3,4,5],[],tick_labels=polnames)

  graph.world.xmax=6.5
  graph.world.ymax=6.5

  graph.world.xmin=0.5
  graph.world.ymin=0.5

  datadict=panel_a(graph)

  for species in datadict:
    for d in datadict[species]:
      graph.add_dataset([(d[0]-0.4*xwidth,d[1]-0.35*ywidth), (d[0]+0.4*xwidth,d[1]+0.35*ywidth)], SolidRectangle, 7*datadict[species][d])

  graph.xaxis.tick.configure(major=1,minor_size=0,major_size=0)
  graph.yaxis.tick.configure(major=1,minor_size=0,major_size=0)

  graph.yaxis.ticklabel.configure(char_size=0,)
  graph.xaxis.ticklabel.configure(char_size=0,place='opposite')

  graph.yaxis.tick.configure(major=1,minor_ticks=1,minor_grid='off')
  graph.xaxis.tick.configure(major=1,minor_ticks=1,minor_grid='off')


  graph.frame.color=0
  graph.xaxis.bar.linewidth=0
  graph.yaxis.bar.linewidth=0


  for x in [0,6]:
    hline=graph.add_drawing_object(DrawLine,start=(.5,.5+x),end=(5.5,.5+x),loctype='world',color=1,linewidth=1,linestyle=1)
  for x in [0,5]:
    vline=graph.add_drawing_object(DrawLine,start=(.5+x,.5),end=(.5+x,6.5),loctype='world',color=1,linewidth=1,linestyle=1)

  graph.panel_label.configure(char_size=0,placement='oul',dy=.03,dx=.04) 


  return graph

def grapher2(grace,graph):
  xwidth=1
  ywidth=1

  names=["A","B","","","",""]
  polnames=[1,2,3,4,5]

  specials=graph.yaxis.tick.set_spec_ticks([6,5,4,3,2,1],[],tick_labels=names)
  specials2=graph.xaxis.tick.set_spec_ticks([1,2,3,4,5],[],tick_labels=polnames)

  graph.world.xmax=6.5
  graph.world.ymax=6.5

  graph.world.xmin=0.5
  graph.world.ymin=0.5

  datadict=panel_a(graph)

  for species in ["A","B"]:
    for d in datadict[species]:
      graph.add_dataset([(d[0]-0.4*xwidth,d[1]-0.35*ywidth), (d[0]+0.4*xwidth,d[1]+0.35*ywidth)], SolidRectangle, 7*datadict[species][d])

  graph.xaxis.tick.configure(major=1,minor_size=0,major_size=0)
  graph.yaxis.tick.configure(major=1,minor_size=0,major_size=0)

  graph.yaxis.ticklabel.configure(char_size=0,)
  graph.xaxis.ticklabel.configure(char_size=0,place='opposite')

  graph.yaxis.tick.configure(major=1,minor_ticks=1,minor_grid='off')
  graph.xaxis.tick.configure(major=1,minor_ticks=1,minor_grid='off')


  graph.frame.color=0
  graph.xaxis.bar.linewidth=0
  graph.yaxis.bar.linewidth=0


  for x in [0,6]:
    hline=graph.add_drawing_object(DrawLine,start=(.5,.5+x),end=(5.5,.5+x),loctype='world',color=1,linewidth=1,linestyle=1)
  for x in [0,5]:
    vline=graph.add_drawing_object(DrawLine,start=(.5+x,.5),end=(.5+x,6.5),loctype='world',color=1,linewidth=1,linestyle=1)

  graph.panel_label.configure(char_size=0,placement='oul',dy=.03,dx=.04) 


  return graph

def grapher3(grace,graph):
  xwidth=1
  ywidth=1

  names=["A","B","","","",""]
  polnames=[1,2,3,4,5]

  specials=graph.yaxis.tick.set_spec_ticks([6,5,4,3,2,1],[],tick_labels=names)
  specials2=graph.xaxis.tick.set_spec_ticks([1,2,3,4,5],[],tick_labels=polnames)

  graph.world.xmax=6.5
  graph.world.ymax=6.5

  graph.world.xmin=0.5
  graph.world.ymin=0.5

  datadict=panel_a(graph)


  for species in ["A","B"]:
    for d in datadict[species]:
      graph.add_dataset([(d[0]-0.4*xwidth,d[1]-0.35*ywidth), (d[0]+0.4*xwidth,d[1]+0.35*ywidth)], SolidRectangle, 7*datadict[species][d])

  graph.xaxis.tick.configure(major=1,minor_size=0,major_size=0)
  graph.yaxis.tick.configure(major=1,minor_size=0,major_size=0)

  graph.yaxis.ticklabel.configure(char_size=0,)
  graph.xaxis.ticklabel.configure(char_size=0,place='opposite')

  graph.yaxis.tick.configure(major=1,minor_ticks=1,minor_grid='off')
  graph.xaxis.tick.configure(major=1,minor_ticks=1,minor_grid='off')


  graph.frame.color=0
  graph.xaxis.bar.linewidth=0
  graph.yaxis.bar.linewidth=0


  for x in [4,6]:
    hline=graph.add_drawing_object(DrawLine,start=(.5,.5+x),end=(5.5,.5+x),loctype='world',color=1,linewidth=1,linestyle=1)
  for x in [0,5]:
    vline=graph.add_drawing_object(DrawLine,start=(.5+x,4.5),end=(.5+x,6.5),loctype='world',color=1,linewidth=1,linestyle=1)


  for species in ["A","B"]:
    for d in datadict[species]:
      if d in [(1,6),(2,6),(1,5),(2,5)]:
        graph.add_dataset([(d[0]-0.4*xwidth,d[1]-3-0.35*ywidth), (d[0]+0.4*xwidth,d[1]-3+0.35*ywidth)], SolidRectangle, 7*datadict[species][d])


  graph.add_drawing_object(DrawText,text='partial overlap', x=3.75, y=2.5, loctype='world',char_size=1.5)

  graph.panel_label.configure(char_size=0,placement='oul',dy=.03,dx=.04) 

  return graph

def grapher4(grace,graph):
  xwidth=1
  ywidth=1

  names=["A","B","","","",""]
  polnames=[1,2,3,4,5]

  specials=graph.yaxis.tick.set_spec_ticks([6,5,4,3,2,1],[],tick_labels=names)
  specials2=graph.xaxis.tick.set_spec_ticks([1,2,3,4,5],[],tick_labels=polnames)

  graph.world.xmax=6.5
  graph.world.ymax=6.5

  graph.world.xmin=0.5
  graph.world.ymin=0.5

  datadict=panel_a(graph)


  for species in ["A","B"]:
    for d in datadict[species]:
      graph.add_dataset([(d[0]-0.4*xwidth,d[1]-0.35*ywidth), (d[0]+0.4*xwidth,d[1]+0.35*ywidth)], SolidRectangle, 7*datadict[species][d])

  graph.xaxis.tick.configure(major=1,minor_size=0,major_size=0)
  graph.yaxis.tick.configure(major=1,minor_size=0,major_size=0)

  graph.yaxis.ticklabel.configure(char_size=0,)
  graph.xaxis.ticklabel.configure(char_size=0,place='opposite')

  graph.yaxis.tick.configure(major=1,minor_ticks=1,minor_grid='off')
  graph.xaxis.tick.configure(major=1,minor_ticks=1,minor_grid='off')


  graph.frame.color=0
  graph.xaxis.bar.linewidth=0
  graph.yaxis.bar.linewidth=0


  for x in [4,6]:
    hline=graph.add_drawing_object(DrawLine,start=(.5,.5+x),end=(5.5,.5+x),loctype='world',color=1,linewidth=1,linestyle=1)
  for x in [0,5]:
    vline=graph.add_drawing_object(DrawLine,start=(.5+x,4.5),end=(.5+x,6.5),loctype='world',color=1,linewidth=1,linestyle=1)


  for species in ["A","B"]:
    for d in datadict[species]:
      if d in [(3,6),(2,6),(3,5),(2,5)]:
        graph.add_dataset([(d[0]-1-0.4*xwidth,d[1]-3-0.35*ywidth), (d[0]-1+0.4*xwidth,d[1]-3+0.35*ywidth)], SolidRectangle, 7*datadict[species][d])


  graph.add_drawing_object(DrawText,text='total overlap', x=3.75, y=2.5, loctype='world',char_size=1.5)

  graph.panel_label.configure(char_size=0,placement='oul',dy=.03,dx=.04) 

  return graph

def grapher5(grace,graph):
  xwidth=1
  ywidth=1

  names=["A","B","","","",""]
  polnames=[1,2,3,4,5]

  specials=graph.yaxis.tick.set_spec_ticks([6,5,4,3,2,1],[],tick_labels=names)
  specials2=graph.xaxis.tick.set_spec_ticks([1,2,3,4,5],[],tick_labels=polnames)

  graph.world.xmax=6.5
  graph.world.ymax=6.5

  graph.world.xmin=0.5
  graph.world.ymin=0.5

  datadict=panel_a(graph)


  for species in ["A","B"]:
    for d in datadict[species]:
      graph.add_dataset([(d[0]-0.4*xwidth,d[1]-0.35*ywidth), (d[0]+0.4*xwidth,d[1]+0.35*ywidth)], SolidRectangle, 7*datadict[species][d])

  graph.xaxis.tick.configure(major=1,minor_size=0,major_size=0)
  graph.yaxis.tick.configure(major=1,minor_size=0,major_size=0)

  graph.yaxis.ticklabel.configure(char_size=0,)
  graph.xaxis.ticklabel.configure(char_size=0,place='opposite')

  graph.yaxis.tick.configure(major=1,minor_ticks=1,minor_grid='off')
  graph.xaxis.tick.configure(major=1,minor_ticks=1,minor_grid='off')


  graph.frame.color=0
  graph.xaxis.bar.linewidth=0
  graph.yaxis.bar.linewidth=0


  for x in [4,6]:
    hline=graph.add_drawing_object(DrawLine,start=(.5,.5+x),end=(5.5,.5+x),loctype='world',color=1,linewidth=1,linestyle=1)
  for x in [0,5]:
    vline=graph.add_drawing_object(DrawLine,start=(.5+x,4.5),end=(.5+x,6.5),loctype='world',color=1,linewidth=1,linestyle=1)


  for species in ["A","B"]:
    for d in datadict[species]:
      if d in [(4,6),(5,6),(4,5),(5,5)]:
        graph.add_dataset([(d[0]-3-0.4*xwidth,d[1]-3-0.35*ywidth), (d[0]-3+0.4*xwidth,d[1]-3+0.35*ywidth)], SolidRectangle, 7*datadict[species][d])


  graph.add_drawing_object(DrawText,text='no overlap', x=3.75, y=2.5, loctype='world',char_size=1.5)

  graph.panel_label.configure(char_size=0,placement='oul',dy=.03,dx=.04) 

  return graph

def grapher6(grace,graph):
  xwidth=1
  ywidth=1

  names=["","","","","",""]
  polnames=[1,2,3,4,5]

  specials=graph.yaxis.tick.set_spec_ticks([6,5,4,3,2,1],[],tick_labels=names)
  specials2=graph.xaxis.tick.set_spec_ticks([1,2,3,4,5],[],tick_labels=polnames)

  graph.world.xmax=8
  graph.world.ymax=6.5

  graph.world.xmin=-2
  graph.world.ymin=-2.5

  datadict=panel_a(graph)

  for species in ["A","B"]:
    for d in datadict[species]:
      graph.add_dataset([(d[0]-0.4*xwidth,d[1]-0.35*ywidth), (d[0]+0.4*xwidth,d[1]+0.35*ywidth)], SolidRectangle, 7*datadict[species][d])

  graph.xaxis.tick.configure(major=1,minor_size=0,major_size=0)
  graph.yaxis.tick.configure(major=1,minor_size=0,major_size=0)

  graph.yaxis.ticklabel.configure(char_size=0,place='normal')
  graph.xaxis.ticklabel.configure(char_size=0,place='opposite')

  graph.yaxis.tick.configure(major=1,minor_ticks=1,minor_grid='off')
  graph.xaxis.tick.configure(major=1,minor_ticks=1,minor_grid='off')


  graph.frame.color=0
  graph.xaxis.bar.linewidth=0
  graph.yaxis.bar.linewidth=0


  for x in [4,6]:
    hline=graph.add_drawing_object(DrawLine,start=(.5,.5+x),end=(5.5,.5+x),loctype='world',color=1,linewidth=1,linestyle=1)
  for x in [0,5]:
    vline=graph.add_drawing_object(DrawLine,start=(.5+x,4.5),end=(.5+x,6.5),loctype='world',color=1,linewidth=1,linestyle=1)

  graph.panel_label.configure(char_size=0,placement='oul',dy=.03,dx=.04) 

  # graph.add_drawing_object(DrawLine,arrow=2,start=(3,4.45),end=(3,3.25),loctype='world')

  return graph

def ABgraph(grace,graph):

  graph.add_drawing_object(DrawLine,arrow=2,start=(-1,10),end=(1,10),loctype='world',linewidth=8)

  xwidth=1
  ywidth=1

  graph.world.xmax=17
  graph.world.ymax=12.25

  graph.world.xmin=1.5
  graph.world.ymin=-.5

  graph.add_drawing_object(DrawText,text='total',x=2,y=10.5,loctype='world',char_size=.75)
  graph.add_drawing_object(DrawBox,lowleft = (5,9.5), upright = (15,12.25),linewidth=1,linestyle=1,loctype='world',fill_color=0)

  graph.add_drawing_object(DrawText,text='partial',x=2,y=5.75,loctype='world',char_size=.75)
  graph.add_drawing_object(DrawBox,lowleft = (5,3), upright = (15,8.75),linewidth=1,linestyle=1,loctype='world',fill_color=0)

  graph.add_drawing_object(DrawText,text='none',x=2,y=.75,loctype='world',char_size=.75)
  graph.add_drawing_object(DrawBox,lowleft = (5,-0.5), upright = (15,2.25),linewidth=1,linestyle=1,loctype='world',fill_color=0)

  # total
  for x in [0,1]:
    graph.add_drawing_object(DrawBox,lowleft = (6+x,10), upright = (6.75+x,10.65),linewidth=1,linestyle=1,loctype='world',fill_color=7,color=7)
    graph.add_drawing_object(DrawBox,lowleft = (6+x,11), upright = (6.75+x,11.65),linewidth=1,linestyle=1,loctype='world',fill_color=7,color=7)


  for y in range(0,2): # 2x med 1
    graph.add_drawing_object(DrawBox,lowleft = (7+3*y,6.5), upright = (7.75+3*y,7.15),linewidth=1,linestyle=1,loctype='world',fill_color=7,color=7)
    for x in [0,1]:
      graph.add_drawing_object(DrawBox,lowleft = (6+x+3*y,7.5), upright = (6.75+x+3*y,8.15),linewidth=1,linestyle=1,loctype='world',fill_color=7,color=7)

  for y in range(0,2): # 2x med 2
    graph.add_drawing_object(DrawBox,lowleft = (12,6.5-3*y), upright = (12.75,7.15-3*y),linewidth=1,linestyle=1,loctype='world',fill_color=7,color=7)
    for x in [0,1]:
      graph.add_drawing_object(DrawBox,lowleft = (12+x,7.5-3*y), upright = (12.75+x,8.15-3*y),linewidth=1,linestyle=1,loctype='world',fill_color=7,color=7)

  for y in range(0,2): # 2x med 3
    graph.add_drawing_object(DrawBox,lowleft = (6+3*y,4.5), upright = (6.75+3*y,5.15),linewidth=1,linestyle=1,loctype='world',fill_color=7,color=7)
    for x in [0,1]:
      graph.add_drawing_object(DrawBox,lowleft = (6+x+3*y,3.5), upright = (6.75+x+3*y,4.15),linewidth=1,linestyle=1,loctype='world',fill_color=7,color=7)

  # none1
  graph.add_drawing_object(DrawBox,lowleft = (6,1), upright = (6.75,1.65),linewidth=1,linestyle=1,loctype='world',fill_color=7,color=7)
  graph.add_drawing_object(DrawBox,lowleft = (7,0), upright = (7.75,.65),linewidth=1,linestyle=1,loctype='world',fill_color=7,color=7)

  # none2
  graph.add_drawing_object(DrawBox,lowleft = (9,1), upright = (9.75,1.65),linewidth=1,linestyle=1,loctype='world',fill_color=7,color=7)
  graph.add_drawing_object(DrawBox,lowleft = (10,1), upright = (10.75,1.65),linewidth=1,linestyle=1,loctype='world',fill_color=7,color=7)

  # none3
  graph.add_drawing_object(DrawBox,lowleft = (12,0), upright = (12.75,.65),linewidth=1,linestyle=1,loctype='world',fill_color=7,color=7)
  graph.add_drawing_object(DrawBox,lowleft = (13,1), upright = (13.75,1.65),linewidth=1,linestyle=1,loctype='world',fill_color=7,color=7)


  graph.xaxis.tick.configure(major=1,minor_size=0,major_size=0)
  graph.yaxis.tick.configure(major=1,minor_size=0,major_size=0)

  graph.yaxis.ticklabel.configure(char_size=0)
  graph.xaxis.ticklabel.configure(char_size=0,place='opposite')

  graph.yaxis.tick.configure(major=1,minor_ticks=1,minor_grid='off')
  graph.xaxis.tick.configure(major=1,minor_ticks=1,minor_grid='off')


  graph.frame.color=0
  graph.xaxis.bar.linewidth=0
  graph.yaxis.bar.linewidth=0

  graph.panel_label.configure(char_size=0,placement='oul',dy=.03,dx=.04) 

  return graph


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


def main():

  colors=ColorBrewerScheme('Purples')
  colors.add_color(200,0,0,"Red")

  grace=Grace(colors=colors)
 
  graph1=grace.add_graph(Panel)

  grapher(grace,graph1)

  grace.write_file('../../manuscript/Figures/Sketches/methods_breakdown_1.eps')

  grace=Grace(colors=colors)
 
  graph1=grace.add_graph(Panel)

  grapher(grace,graph1)
  graph1.add_drawing_object(DrawBox,lowleft=(0.55,4.55),upright=(5.45,6.425),color=1,loctype='world',fill_color=0,fill_pattern=0,linestyle=3,linewidth=2)

  grace.write_file('../../manuscript/Figures/Sketches/methods_breakdown_1a.eps')

  grace=Grace(colors=colors)
 
  graph1=grace.add_graph(Panel)

  grapher2(grace,graph1)
  # graph1.add_drawing_object(DrawBox,lowleft=(0.55,4.55),upright=(5.45,6.425),color=1,loctype='world',fill_color=0,fill_pattern=0,linestyle=3,linewidth=2)
  grace.write_file('../../manuscript/Figures/Sketches/methods_breakdown_1b.eps')

  grace=Grace(colors=colors)
 
  graph1=grace.add_graph(Panel)

  grapher2(grace,graph1)
  graph1.add_drawing_object(DrawBox,lowleft=(0.55,4.55),upright=(2.45,6.425),color=1,loctype='world',fill_color=0,fill_pattern=0,linestyle=3,linewidth=2)
  grace.write_file('../../manuscript/Figures/Sketches/methods_breakdown_1c.eps')

  grace=Grace(colors=colors)
 
  graph1=grace.add_graph(Panel)

  grapher3(grace,graph1)
  graph1.add_drawing_object(DrawBox,lowleft=(0.55,4.55),upright=(2.45,6.425),color=1,loctype='world',fill_color=0,fill_pattern=0,linestyle=3,linewidth=2)
  grace.write_file('../../manuscript/Figures/Sketches/methods_breakdown_partial.eps')

  grace=Grace(colors=colors)
 
  graph1=grace.add_graph(Panel)

  grapher4(grace,graph1)
  graph1.add_drawing_object(DrawBox,lowleft=(1.55,4.55),upright=(3.45,6.425),color=1,loctype='world',fill_color=0,fill_pattern=0,linestyle=3,linewidth=2)
  grace.write_file('../../manuscript/Figures/Sketches/methods_breakdown_total.eps')

  grace=Grace(colors=colors)
 
  graph1=grace.add_graph(Panel)

  grapher5(grace,graph1)
  graph1.add_drawing_object(DrawBox,lowleft=(3.55,4.55),upright=(5.45,6.425),color=1,loctype='world',fill_color=0,fill_pattern=0,linestyle=3,linewidth=2)
  grace.write_file('../../manuscript/Figures/Sketches/methods_breakdown_none.eps')

  grace=MultiPanelGrace(colors=colors)
 
  graph1=grace.add_graph(Panel)

  grapher2(grace,graph1)

  graph2=grace.add_graph(Panel)
  ABgraph(grace,graph2)

  grace.multi(rows=2,cols=2,hgap=.03)

  grace.write_file('../../manuscript/Figures/Sketches/methods_breakdown_vector_1.eps')

  grace=MultiPanelGrace(colors=colors)
 
  graph1=grace.add_graph(Panel)

  grapher2(grace,graph1)

  graph2=grace.add_graph(Panel)
  ABgraph(grace,graph2)

  grace.multi(rows=2,cols=2,hgap=.03)

  graph1.add_drawing_object(DrawText,text='total: 1', x=1, y=3, just=0, loctype='world',char_size=1)
  graph1.add_drawing_object(DrawText,text='partial: 6', x=1, y=2, just=0, loctype='world',char_size=1)
  graph1.add_drawing_object(DrawText,text='none: 3', x=1, y=1, just=0, loctype='world',char_size=1)

  grace.write_file('../../manuscript/Figures/Sketches/methods_breakdown_vector_2.eps')

  grace=MultiPanelGrace(colors=colors)
 
  graph1=grace.add_graph(Panel)

  grapher2(grace,graph1)

  graph2=grace.add_graph(Panel)
  ABgraph(grace,graph2)

  grace.multi(rows=2,cols=2,hgap=.03)

  graph1.add_drawing_object(DrawText,text='total: 1', x=1, y=3, just=0, loctype='world',char_size=1)
  graph1.add_drawing_object(DrawText,text='partial: 6', x=1, y=2, just=0, loctype='world',char_size=1)
  graph1.add_drawing_object(DrawText,text='none: 3', x=1, y=1, just=0, loctype='world',char_size=1)

  graph1.add_drawing_object(DrawText,text='distance: 30 My', x=2.75, y=3, just=0, loctype='world',char_size=1)

  grace.write_file('../../manuscript/Figures/Sketches/methods_breakdown_vector_3.eps')

  grace=Grace(colors=colors)
 
  graph1=grace.add_graph(Panel)

  vectorgrapher(grace,graph1)
  grace.write_file('../../manuscript/Figures/Sketches/methods_breakdown_manyvectors.eps')



if __name__ == '__main__':
  main()
