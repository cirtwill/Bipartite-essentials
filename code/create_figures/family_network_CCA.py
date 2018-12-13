import sys
import math
import random
from decimal import *


#Giulio says there's something wrong with the cca that explains the wierd shape?
# I think I would like two panels, for early and late, please.

#Pygrace libraries
from PyGrace.grace import Grace
from PyGrace.colors import RandomColorScheme, MarkovChainColorScheme, ColorBrewerScheme
from PyGrace.dataset import SYMBOLS
from PyGrace.Extensions.panel import Panel,MultiPanelGrace
from PyGrace.drawing_objects import DrawText, DrawLine

from PyGrace.Extensions.distribution import CDFGraph, PDFGraph
from PyGrace.Extensions.latex_string import LatexString, CONVERT

colors=ColorBrewerScheme('Spectral')#,reverse=True)  # The blue is very beautiful but maybe harder to see.

pointsize=1

def pointreader(netfile):

  pointdict={'ph':[],'pp':[]}

  f=open(netfile,'r')
  for line in f:
    if line.split()[0] not in ['"V1"','""','"MDS1"','"CCA1"','"CA1"']:
      rownum=line.split()[0][1:-1]
      if rownum < 9: 
        nettype='ph'
      else:
        nettype='pp'
      x=float(line.split()[1])#[1:-1])
      y=float(line.split()[2])#[1:-1])

      pointdict[nettype].append((x,y))

  f.close()
  return pointdict

def famreader(famfile):
  points={}
  f=open(famfile,'r')
  i=1
  for line in f:
    if line.split()[0] not in ['"CCA1"','"CA1"','"MDS1"']:
      family=line.split()[0][1:-1]
      print family
      x=float(line.split()[1])
      y=float(line.split()[2])
      points[family]=[(x,y)]
      i=i+1
  f.close()

  return points

def points(graph,pointdict):
  for group in pointdict:
    points=pointdict[group]
    pointy=graph.add_dataset(points)
    pointy.line.linestyle=0
    if group=='ph':
      col=12
    else:
      col=2
    pointy.symbol.configure(shape=1,fill_color=col,linewidth=1,size=pointsize*.5)
  return graph


def legendary(graph,group):
  if group=='early':
    for month in ['1996','1997','2010','2011']:
      dummy=graph.add_dataset([(9,9)])
      dummy.line.linestyle=0
      if month=='1996':
        col=12
      elif month=='1997':
        col=10
      elif month=='2010':
        col=4
      else:
        col=2
      dummy.symbol.configure(shape=1,fill_color=col,linewidth=1,size=pointsize*.75)
      dummy.legend=month

  return graph
 

graphtype='blarg'

grace=Grace(colors=colors)

graph=grace.add_graph()

graph.yaxis.bar.linewidth=1
graph.xaxis.bar.linewidth=1
graph.frame.linewidth=1
graph.world.xmin=-2
graph.world.xmax=8
graph.world.ymin=-8
graph.world.ymax=1

legend=0
graph.legend.configure(loc=(-1.4,-.4),char_size=.75,loctype='world',box_linestyle=0,box_fill=0)

if legend==1:
  graph=legendary(graph,group)

graph.yaxis.ticklabel.configure(char_size=.75,format='decimal',prec=1)
graph.xaxis.ticklabel.configure(char_size=.75,format='decimal',prec=0)
graph.xaxis.tick.configure(major=1,onoff='on',minor_ticks=1,major_size=.7,place='both',minor_size=.5,major_linewidth=1,minor_linewidth=1)
graph.yaxis.tick.configure(major=.5,onoff='on',minor_ticks=1,major_size=.7,place='both',minor_size=.5,major_linewidth=1,minor_linewidth=1)


graph.xaxis.label.configure(text="First CA axis (%)",char_size=1)
graph.yaxis.label.configure(text="Second CA axis (%)",char_size=1)

pointdict=pointreader('../../data/families_to_networks/network_CCA_positions.tsv')

graph=points(graph,pointdict)

fampoints=famreader('../../data/families_to_networks/family_CCA_positions.tsv')
for family in fampoints:
  graph.add_drawing_object(DrawText,text=str(family),x=fampoints[family][0][0],y=fampoints[family][0][1],loctype='world',char_size=.5)


grace.write_file('../../manuscript/Figures/family_network_CCA.eps')
