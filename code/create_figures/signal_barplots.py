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

from PyGrace.Extensions.distribution import CDFGraph, PDFGraph
from PyGrace.Extensions.latex_string import LatexString, CONVERT

def signalreader(datapath,sig):
  databank={'ph':{},'pp':{}}
  f=open(datapath,'r')
  for line in f:
    line2=line.split('\n')[0]
    newline=line2.split(',')
    if len(newline)==5 or len(newline)==7:
      x=int(newline[0][1:-1])
      netname=newline[1][1:-1]
      nettype=newline[2][1:-1]
      if sig!='degree':
        K=float(newline[3][1:-1])
        p=float(newline[4][1:-1])
      else:
        K=float(newline[5][1:-1])
        p=float(newline[6][1:-1])
      databank[nettype][x]=((K,p,netname))
  f.close()
  return databank

def indiv_plot(sig,plottype,datapath):

  grace=Grace(colors=ColorBrewerScheme('PRGn'))
  graph=grace.add_graph()

  ppset=[]
  phset=[]
  ys=[]
  if plottype!='axis':
    databank=signalreader(datapath,sig)

    if plottype=='one':
      net=65
      ppset.append((70-net,1-databank['pp'][net][1]))
    else:
      for net in databank['pp']:
        ys.append((1-databank['pp'][net][1],'pp'))

    if plottype=='full':
      for net in databank['ph']:
        ys.append((1-databank['ph'][net][1],'ph'))

    for i in range(0,len(sorted(ys))):
      if sorted(ys,reverse=True)[i][1]=='pp':
        ppset.append((i+2,sorted(ys,reverse=True)[i][0]))
      elif sorted(ys,reverse=True)[i][1]=='ph':
        phset.append((i+2,sorted(ys,reverse=True)[i][0]))
    phdata=graph.add_dataset(phset,type='bar')
    phdata.line.linestyle=0
    phdata.symbol.configure(fill_color=9,size=.5)
    phdata.legend='Plant-herbivore network'
      
    ppdata=graph.add_dataset(ppset,type='bar')
    ppdata.line.linestyle=0
    ppdata.symbol.configure(fill_color=3,size=.5)
    ppdata.legend='Plant-pollinator network'

  # print sig
  # print sorted(phset)
  # print sorted(ppset)
  sigline=graph.add_drawing_object(DrawLine,start=(0,0.95),end=(70,0.95),linestyle=2,linewidth=2,loctype='world')

  datalen=len(ppset)+len(phset)

  # print datalen

  graph.world.xmin=0
  graph.world.xmax=70

  graph.world.ymin=0
  graph.world.ymax=1

  graph.frame.linewidth=1.5
  graph.xaxis.bar.linewidth=1.5
  graph.yaxis.bar.linewidth=1.5

  graph.legend.configure(loc=(45,.9),loctype='world',char_size=.75,box_linestyle=0)

  
  if sig=='degree':
    graph.xaxis.label.configure(text='Degree',char_size=1)
  elif sig=='mantel':
    graph.xaxis.label.configure(text='Matrix similarity',char_size=1)    
  else:
    graph.xaxis.label.configure(text='Partners',char_size=1)

  graph.yaxis.label.configure(text='Phylogenetic signal (1-p)',char_size=1)

  graph.yaxis.tick.configure(place='both',major_size=.7,major=.1,major_linewidth=1.5,minor_linewidth=1.5,minor_size=.4)
  graph.yaxis.ticklabel.configure(char_size=.85,format='decimal',prec=1,just=0)
  graph.xaxis.tick.configure(place='normal',major_size=0,minor_ticks=0,major=1,major_linewidth=1.5)
  graph.xaxis.ticklabel.configure(char_size=0)

  grace.write_file('../../manuscript/Figures/dataplots/'+sig+'_'+plottype+'.eps')

def main():

  directory='../../data/'
  sigtypes=['degree','partners','mantel']

  for sig in sigtypes:
    for plottype in ['axis','one','pp','full']:
      datapath=directory+'bynetwork_signal_'+sig+'.csv'
      indiv_plot(sig,plottype,datapath)

if __name__ == '__main__':
  main()
