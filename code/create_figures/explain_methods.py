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

def grapher(grace,graph):
  names=["A","B","C","D","E","F"]
  polnames=[1,2,3,4,5]

  specials=graph.yaxis.tick.set_spec_ticks([6,5,4,3,2,1],[],tick_labels=names)
  specials2=graph.xaxis.tick.set_spec_ticks([1,2,3,4,5],[],tick_labels=polnames)

  graph.world.xmax=5.5
  graph.world.ymax=6.5

  graph.world.xmin=0.5
  graph.world.ymin=0.5

  boxes=[(1,1),(1,2),(1,3),(1,4),(1,6),(2,3),(2,4),(2,5),(2,6),(3,5),(3,6),(4,3),(4,4),(4,5),(5,6)]

  boxed=graph.add_dataset(boxes)
  boxed.line.linestyle=0
  boxed.symbol.configure(shape=2,size=4,fill_color=8)

  graph.xaxis.tick.configure(major=1,minor_size=0,major_size=0)
  graph.yaxis.tick.configure(major=1,minor_size=0,major_size=0)

  graph.yaxis.ticklabel.configure(char_size=1)
  graph.xaxis.ticklabel.configure(char_size=1,place='opposite')

  graph.yaxis.tick.configure(major=1,minor_ticks=1,minor_grid='off')
  graph.xaxis.tick.configure(major=1,minor_ticks=1,minor_grid='off')

  graph.frame.color=1
  graph.xaxis.bar.linewidth=0
  graph.yaxis.bar.linewidth=0
  graph.panel_label.configure(char_size=0,placement='oul',dy=.03,dx=.04) 
  return graph

def ABgrapher(grace,graph):
  xwidth=1
  ywidth=1

  graph.world.xmax=27.5
  graph.world.ymax=18

  graph.world.xmin=1
  graph.world.ymin=6

  graph.add_drawing_object(DrawText,text=\
    LatexString(r'Total\noverlap'),x=0,y=16,loctype='world',char_size=1.25)
  graph.add_drawing_object(DrawBox,lowleft = (3.5,14.25), upright = (27,17.5),linewidth=1,linestyle=1,loctype='world',fill_color=0,fill_pattern=0)

  graph.add_drawing_object(DrawText,text=\
    LatexString(r'Partial\noverlap'),x=0,y=12,loctype='world',char_size=1.25)
  graph.add_drawing_object(DrawBox,lowleft = (3.5,10.25), upright = (27,13.5),linewidth=1,linestyle=1,loctype='world',fill_color=0,fill_pattern=0)

  graph.add_drawing_object(DrawText,text=\
    LatexString(r'No\noverlap'),x=0,y=8,loctype='world',char_size=1.25)
  graph.add_drawing_object(DrawBox,lowleft = (3.5,6.25), upright = (27,9.5),linewidth=1,linestyle=1,loctype='world',fill_color=0,fill_pattern=0)

  # TOTAL OVERLAP

  highbox=[(5,16),(6,16),(5,15),(6,15)]
  highboxed=graph.add_dataset(highbox)
  highboxed.line.linestyle=0
  highboxed.symbol.configure(shape=2,size=1.5,fill_color=8)

  graph.add_drawing_object(DrawText,text='2',x=5,y=16.75,loctype='world',just=2,char_size=1)
  graph.add_drawing_object(DrawText,text='3',x=6,y=16.75,loctype='world',just=2,char_size=1)
  graph.add_drawing_object(DrawText,text='A',x=4.25,y=15.75,loctype='world',just=2,char_size=1)
  graph.add_drawing_object(DrawText,text='B',x=4.25,y=14.75,loctype='world',just=2,char_size=1)


  # PARTIAL OVERLAP

  medbox=[(5,12),(6,12),(6,11),
          (9,12),(10,12),(10,11),
          (13,12),(14,12),(13,11),
          (17,12),(18,12),(17,11),
          (21,12),(21,11),(22,11),
          (25,12),(25,11),(26,11)  ]
  medboxed=graph.add_dataset(medbox)
  medboxed.line.linestyle=0
  medboxed.symbol.configure(shape=2,size=1.5,fill_color=8)

  graph.add_drawing_object(DrawText,text='1',x=5,y=12.75,loctype='world',just=2,char_size=1)
  graph.add_drawing_object(DrawText,text='2',x=6,y=12.75,loctype='world',just=2,char_size=1)
  graph.add_drawing_object(DrawText,text='A',x=4.25,y=11.75,loctype='world',just=2,char_size=1)
  graph.add_drawing_object(DrawText,text='B',x=4.25,y=10.75,loctype='world',just=2,char_size=1)

  graph.add_drawing_object(DrawText,text='1',x=9,y=12.75,loctype='world',just=2,char_size=1)
  graph.add_drawing_object(DrawText,text='3',x=10,y=12.75,loctype='world',just=2,char_size=1)
  graph.add_drawing_object(DrawText,text='A',x=8.25,y=11.75,loctype='world',just=2,char_size=1)
  graph.add_drawing_object(DrawText,text='B',x=8.25,y=10.75,loctype='world',just=2,char_size=1)

  graph.add_drawing_object(DrawText,text='2',x=13,y=12.75,loctype='world',just=2,char_size=1)
  graph.add_drawing_object(DrawText,text='5',x=14,y=12.75,loctype='world',just=2,char_size=1)
  graph.add_drawing_object(DrawText,text='A',x=12.25,y=11.75,loctype='world',just=2,char_size=1)
  graph.add_drawing_object(DrawText,text='B',x=12.25,y=10.75,loctype='world',just=2,char_size=1)

  graph.add_drawing_object(DrawText,text='3',x=17,y=12.75,loctype='world',just=2,char_size=1)
  graph.add_drawing_object(DrawText,text='5',x=18,y=12.75,loctype='world',just=2,char_size=1)
  graph.add_drawing_object(DrawText,text='A',x=16.25,y=11.75,loctype='world',just=2,char_size=1)
  graph.add_drawing_object(DrawText,text='B',x=16.25,y=10.75,loctype='world',just=2,char_size=1)

  graph.add_drawing_object(DrawText,text='2',x=21,y=12.75,loctype='world',just=2,char_size=1)
  graph.add_drawing_object(DrawText,text='4',x=22,y=12.75,loctype='world',just=2,char_size=1)
  graph.add_drawing_object(DrawText,text='A',x=20.25,y=11.75,loctype='world',just=2,char_size=1)
  graph.add_drawing_object(DrawText,text='B',x=20.25,y=10.75,loctype='world',just=2,char_size=1)

  graph.add_drawing_object(DrawText,text='3',x=25,y=12.75,loctype='world',just=2,char_size=1)
  graph.add_drawing_object(DrawText,text='4',x=26,y=12.75,loctype='world',just=2,char_size=1)
  graph.add_drawing_object(DrawText,text='A',x=24.25,y=11.75,loctype='world',just=2,char_size=1)
  graph.add_drawing_object(DrawText,text='B',x=24.25,y=10.75,loctype='world',just=2,char_size=1)


  # NO OVERLAP

  lowbox=[(5,8),(6,7),
          (9,8),(10,8),
          (14,8),(13,7)]
  lowboxed=graph.add_dataset(lowbox)
  lowboxed.line.linestyle=0
  lowboxed.symbol.configure(shape=2,size=1.5,fill_color=8)

  graph.add_drawing_object(DrawText,text='1',x=5,y=8.75,loctype='world',just=2,char_size=1)
  graph.add_drawing_object(DrawText,text='4',x=6,y=8.75,loctype='world',just=2,char_size=1)
  graph.add_drawing_object(DrawText,text='A',x=4.25,y=7.75,loctype='world',just=2,char_size=1)
  graph.add_drawing_object(DrawText,text='B',x=4.25,y=6.75,loctype='world',just=2,char_size=1)

  graph.add_drawing_object(DrawText,text='1',x=9,y=8.75,loctype='world',just=2,char_size=1)
  graph.add_drawing_object(DrawText,text='5',x=10,y=8.75,loctype='world',just=2,char_size=1)
  graph.add_drawing_object(DrawText,text='A',x=8.25,y=7.75,loctype='world',just=2,char_size=1)
  graph.add_drawing_object(DrawText,text='B',x=8.25,y=6.75,loctype='world',just=2,char_size=1)

  graph.add_drawing_object(DrawText,text='4',x=13,y=8.75,loctype='world',just=2,char_size=1)
  graph.add_drawing_object(DrawText,text='5',x=14,y=8.75,loctype='world',just=2,char_size=1)
  graph.add_drawing_object(DrawText,text='A',x=12.25,y=7.75,loctype='world',just=2,char_size=1)
  graph.add_drawing_object(DrawText,text='B',x=12.25,y=6.75,loctype='world',just=2,char_size=1)



  graph.yaxis.ticklabel.configure(char_size=0)
  graph.xaxis.ticklabel.configure(char_size=0)
  graph.yaxis.tick.configure(onoff='off')
  graph.xaxis.tick.configure(onoff='off')
  graph.frame.color=0
  graph.xaxis.bar.linewidth=0
  graph.yaxis.bar.linewidth=0

  graph.panel_label.configure(char_size=0,placement='oul',dy=.03,dx=.04) 

  return graph

def shellgrapher(grace,graph,pattern):
  names=["A","B","C","D","E","F"]
  names2=["F",'E','D','C','B','A']
  polnames=[1,2,3,4,5]

  specials=graph.yaxis.tick.set_spec_ticks([6,5,4,3,2,1],[],tick_labels=names)
  specials2=graph.xaxis.tick.set_spec_ticks([6,5,4,3,2,1],[],tick_labels=names2)

  # Add diagonal lines
  if pattern=='total':
    total_points(grace,graph)
    graph.add_drawing_object(DrawText, text='Total overlap', char_size=1.5,just=2,x=3.5,y=7.25,loctype='world')
  elif pattern=='none':
    none_points(grace,graph)
    graph.add_drawing_object(DrawText, text='No overlap', char_size=1.5,just=2,x=3.5,y=7.25,loctype='world')
  else:
    partial_points(grace,graph)
    graph.add_drawing_object(DrawText, text='Partial overlap', char_size=1.5,just=2,x=3.5,y=7.25,loctype='world')

  for i in range(1,7):
    graph.add_drawing_object(DrawText,x=i,y=7-i,text='-',char_size=1,loctype='world')


  graph.world.xmax=6.5
  graph.world.ymax=6.5

  graph.world.xmin=0.5
  graph.world.ymin=0.5

  graph.xaxis.tick.configure(major=1,minor_size=0,major_size=0)
  graph.yaxis.tick.configure(major=1,minor_size=0,major_size=0)

  graph.yaxis.ticklabel.configure(char_size=1)
  graph.xaxis.ticklabel.configure(char_size=1,place='opposite')

  graph.yaxis.tick.configure(major=1,minor_ticks=1,minor_grid='off')
  graph.xaxis.tick.configure(major=1,minor_ticks=1,minor_grid='off')

  graph.frame.color=1
  graph.xaxis.bar.linewidth=0
  graph.yaxis.bar.linewidth=0
  graph.panel_label.configure(char_size=0,placement='oul',dy=.03,dx=.04) 
  return graph

def total_points(grace,graph):

  # A, B, C, D mutually share one.
  for i in range(2,5):
    graph.add_drawing_object(DrawText,x=i,y=6,text='1',char_size=1,loctype='world')
    graph.add_drawing_object(DrawText,x=1,y=7-i,text='1',char_size=1,loctype='world')

  for i in range(3,5):
    graph.add_drawing_object(DrawText,x=i,y=5,text='1',char_size=1,loctype='world')
    graph.add_drawing_object(DrawText,x=2,y=7-i,text='1',char_size=1,loctype='world')

  for i in range(4,5):
    graph.add_drawing_object(DrawText,x=i,y=4,text='1',char_size=1,loctype='world')
    graph.add_drawing_object(DrawText,x=3,y=7-i,text='1',char_size=1,loctype='world')

  # E and F
  for i in range(1,5):
    graph.add_drawing_object(DrawText,x=i,y=1,text='0',char_size=1,loctype='world')
    graph.add_drawing_object(DrawText,x=i,y=2,text='0',char_size=1,loctype='world')
    graph.add_drawing_object(DrawText,x=5,y=7-i,text='0',char_size=1,loctype='world')
    graph.add_drawing_object(DrawText,x=6,y=7-i,text='0',char_size=1,loctype='world')

  # EF
  graph.add_drawing_object(DrawText,x=5,y=1,text='1',char_size=1,loctype='world')
  graph.add_drawing_object(DrawText,x=6,y=2,text='1',char_size=1,loctype='world')

  return graph

def none_points(grace,graph):

  #A: - 3 3 3 0 0
  #B: 3 - 1 1 6 6
  #C: 3 1 - 0 1 1
  #D: 3 1 0 - 1 1
  #E: 0 6 1 1 - 0
  #F: 0 6 1 1 0 -

  for i in range(2,5):
    graph.add_drawing_object(DrawText,x=i,y=6,text='3',char_size=1,loctype='world')
    graph.add_drawing_object(DrawText,x=1,y=7-i,text='3',char_size=1,loctype='world')

  for i in range(5,7):
    graph.add_drawing_object(DrawText,x=i,y=6,text='0',char_size=1,loctype='world')
    graph.add_drawing_object(DrawText,x=1,y=7-i,text='0',char_size=1,loctype='world')

  for i in range(3,5):
    graph.add_drawing_object(DrawText,x=i,y=5,text='1',char_size=1,loctype='world')
    graph.add_drawing_object(DrawText,x=2,y=7-i,text='1',char_size=1,loctype='world')

  for i in range(5,7):
    graph.add_drawing_object(DrawText,x=i,y=5,text='6',char_size=1,loctype='world')
    graph.add_drawing_object(DrawText,x=2,y=7-i,text='6',char_size=1,loctype='world')

  graph.add_drawing_object(DrawText,x=3,y=3,text='0',char_size=1,loctype='world')
  graph.add_drawing_object(DrawText,x=4,y=4,text='0',char_size=1,loctype='world')

  # # EF and CD
  for i in range(3,5):
    graph.add_drawing_object(DrawText,x=i,y=1,text='1',char_size=1,loctype='world')
    graph.add_drawing_object(DrawText,x=i,y=2,text='1',char_size=1,loctype='world')
    graph.add_drawing_object(DrawText,x=5,y=7-i,text='1',char_size=1,loctype='world')
    graph.add_drawing_object(DrawText,x=6,y=7-i,text='1',char_size=1,loctype='world')

  # # EF
  graph.add_drawing_object(DrawText,x=5,y=1,text='0',char_size=1,loctype='world')
  graph.add_drawing_object(DrawText,x=6,y=2,text='0',char_size=1,loctype='world')

def partial_points(grace,graph):
  #A: - 6 6 6 3 3
  #B: 6 - 4 4 0 0
  #C: 6 4 - 0 2 2
  #D: 6 4 0 - 2 2
  #E: 3 0 2 2 - 0
  #F: 3 0 2 2 0 -

  for i in range(2,5):
    graph.add_drawing_object(DrawText,x=i,y=6,text='6',char_size=1,loctype='world')
    graph.add_drawing_object(DrawText,x=1,y=7-i,text='6',char_size=1,loctype='world')

  for i in range(5,7):
    graph.add_drawing_object(DrawText,x=i,y=6,text='3',char_size=1,loctype='world')
    graph.add_drawing_object(DrawText,x=1,y=7-i,text='3',char_size=1,loctype='world')

  for i in range(3,5):
    graph.add_drawing_object(DrawText,x=i,y=5,text='4',char_size=1,loctype='world')
    graph.add_drawing_object(DrawText,x=2,y=7-i,text='4',char_size=1,loctype='world')

  for i in range(5,7):
    graph.add_drawing_object(DrawText,x=i,y=5,text='0',char_size=1,loctype='world')
    graph.add_drawing_object(DrawText,x=2,y=7-i,text='0',char_size=1,loctype='world')

  graph.add_drawing_object(DrawText,x=3,y=3,text='0',char_size=1,loctype='world')
  graph.add_drawing_object(DrawText,x=4,y=4,text='0',char_size=1,loctype='world')

  # # EF and CD
  for i in range(3,5):
    graph.add_drawing_object(DrawText,x=i,y=1,text='2',char_size=1,loctype='world')
    graph.add_drawing_object(DrawText,x=i,y=2,text='2',char_size=1,loctype='world')
    graph.add_drawing_object(DrawText,x=5,y=7-i,text='2',char_size=1,loctype='world')
    graph.add_drawing_object(DrawText,x=6,y=7-i,text='2',char_size=1,loctype='world')

  # # EF
  graph.add_drawing_object(DrawText,x=5,y=1,text='0',char_size=1,loctype='world')
  graph.add_drawing_object(DrawText,x=6,y=2,text='0',char_size=1,loctype='world')


def main():

  colors=ColorBrewerScheme('Purples')
  colors.add_color(200,0,0,"Red")

  grace=MultiPanelGrace(colors=colors)
  grace.add_label_scheme("dummy",['(a)','(b)','(c)','(d)','(e)'])
  grace.set_label_scheme("dummy")

  graph1=grace.add_graph(Panel)

  grapher(grace,graph1)

  graph1.add_drawing_object(DrawBox,lowleft=(0.45,4.45),upright=(5.55,6.55),color=1,loctype='world',fill_color=0,fill_pattern=0,linestyle=3,linewidth=1)

  print graph1.get_view()
  graph1.set_view(0.1,0.7,0.6,1.2)

  graph2=grace.add_graph(Panel)
  ABgrapher(grace,graph2)
  graph2.add_drawing_object(DrawLine,loctype='world',start=(-3.5,16),end=(-1,13),arrow=2,arrow_type=0,linewidth=10)

  graph2.add_drawing_object(DrawLine,loctype='world',start=(11,5),end=(-7,1),arrow=2,arrow_type=0,linewidth=10)
  graph2.add_drawing_object(DrawLine,loctype='world',start=(11,5),end=(6,1),arrow=2,arrow_type=0,linewidth=10)
  graph2.add_drawing_object(DrawLine,loctype='world',start=(10.9,5.03),end=(18,1),arrow=2,arrow_type=0,linewidth=10)

  print graph2.get_view()
  # graph2.set_view()
  graph2.set_view(0.8,0.8,1.8,1.2)

  graph3=grace.add_graph(Panel)
  shellgrapher(grace,graph3,'total')
  graph3.set_view(0.2,0.1,0.6,0.5)

  # ADDING DISTANCES TO THE 4TH PANEL
  graph4=grace.add_graph(Panel)
  shellgrapher(grace,graph4,'partial')
  graph4.set_view(0.75,0.1,1.15,0.5)

  graph5=grace.add_graph(Panel)
  shellgrapher(grace,graph5,'none')
  graph5.set_view(1.3,0.1,1.7,0.5)

  for graph in [graph1,graph2,graph3,graph4,graph5]:
    graph.panel_label.configure(char_size=1.5,fontset=6,font=6)

  grace.write_file('../../manuscript/Figures/Sketches/methods_breakdown.eps')
  # grace.write_file('../../manuscript/Figures/Sketches/methods_breakdown.jpg')


if __name__ == '__main__':
  main()
