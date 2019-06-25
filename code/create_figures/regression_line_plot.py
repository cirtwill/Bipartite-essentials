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

scaledict={'centre':251.7093,'scale':91.05211}

def signalreader(datapath,suffix):
  databank={'fixef':{},'ranef':{}}
  f=open(datapath+suffix+'_fixef.tsv','r')
  for line in f:
    if line.split()[0]!='"Estimate"':
      name=line.split()[0][1:-1]
      effect=float(line.split()[1])
      databank['fixef'][name]=effect
  f.close()
 
  ran=open(datapath+suffix+'_ranef.tsv','r')
  for line in ran:
    if len(line.split())==3:
      network=line.split()[0][1:-1]
      intercept=float(line.split()[1])
      slope=float(line.split()[2])
      databank['ranef'][network]=(intercept,slope)
  ran.close()

  return databank

def simlines_scaled(inter,beta):
  simdata=[]
  for i in range(0,80):
    dist=10*i
    scaledist=(dist-scaledict['centre'])/scaledict['scale']
    y=inter+scaledist*beta
    logity=1/(1+math.exp(0-y))
    simdata.append((dist,logity))
  return simdata

def format_graph(graph,rowtype,colormode):
  print rowtype
  graphtype='full'

  if rowtype=='ph':
    ytext='Proportion of shared herbivores'
  else:
    ytext='Proportion of shared pollinators'

  graph.yaxis.label.configure(text=ytext,char_size=0.85,just=2)
  graph.world.xmax=800
  major=200
  prec=0

  graph.world.ymax=0.60000000001
  graph.yaxis.tick.configure(place='both',major_size=.4,minor_ticks=1,minor_size=.2,major=.2,major_linewidth=1,minor_linewidth=1)

  graph.yaxis.ticklabel.configure(char_size=.75,format='decimal',prec=1)
  graph.xaxis.tick.configure(place='both',major_size=.4,minor_ticks=1,minor_size=.2,major=major,major_linewidth=1,minor_linewidth=1)
  graph.xaxis.ticklabel.configure(char_size=.75,format='decimal',prec=prec)

  graph.frame.linewidth=1
  graph.xaxis.bar.linewidth=1
  graph.yaxis.bar.linewidth=1
  
  graph.panel_label.configure(char_size=.85,placement='iuc',dy=0.01,dx=0,just=2)

  return graph

def lineplotter(grace,datapath,modeltype,colormode):

  suffix='_reg_unranked_scaled'

  for rowtype in ['ph','pp']:
    # Looks like these are supposed to be overall regs?
    databank=signalreader(datapath,suffix)
    graph=grace.add_graph(Panel)
    graph=format_graph(graph,rowtype,colormode)

    fdatabank=databank['fixef']

    ppinter=fdatabank['(Intercept)']+fdatabank['nettypepp'] #Because R loves to alphabetise :(
    ppbeta=fdatabank['scale(distance)']+fdatabank['scale(distance):nettypepp']
    pp_simdata=simlines_scaled(ppinter,ppbeta)
    print('pp lines ok')

    # Now add the overall effect for ph webs
    phinter=fdatabank['(Intercept)']
    phbeta=fdatabank['scale(distance)']
    ph_simdata=simlines_scaled(phinter,phbeta)
    print('ph lines ok')

    for network in databank['ranef']:
      subfolder=network.split('-')[0].split('/')[0]
      if subfolder=='Stouffer_Ecology_Matrices':
        nettype='pp'
      else:
        nettype='ph'
      if nettype==rowtype:
        if nettype=='pp':
          inter=ppinter+databank['ranef'][network][0]
          beta=ppbeta+databank['ranef'][network][1]
          data=simlines_scaled(inter,beta)

          dat=graph.add_dataset(data)
          dat.symbol.shape=0
          if colormode=='grey':
            dat.line.configure(linestyle=1,linewidth=1,color=6)
          else:
            dat.line.configure(linestyle=1,linewidth=1,color=4)

        else:
          inter=phinter+databank['ranef'][network][0]
          beta=phbeta+databank['ranef'][network][1]
          data=simlines_scaled(inter,beta)

          dat=graph.add_dataset(data)
          dat.symbol.shape=0
          if colormode=='grey':
            dat.line.configure(linestyle=1,linewidth=1,color=6)
          else:
            dat.line.configure(linestyle=1,linewidth=1,color=10)

    # Add thick overall lines
	for dataset in [eval(rowtype+'_simdata')]:
	  if colormode=='grey':
	    linecol=9
	  else:
	    if dataset==pp_simdata:
	      linecol=2
	    else:
	      linecol=11
	  dat=graph.add_dataset(dataset)
	  dat.symbol.shape=0
	  dat.line.configure(linestyle=1,linewidth=4,color=linecol)

  return grace

def main():
  graphtype='full'
  modeltype='scaled'
  colormode='color'

  datapath='../../data/Jaccard/Observed_regression/overall_bynetwork'
  if colormode=='grey':
    grace=MultiPanelGrace(colors=ColorBrewerScheme('Greys'))
  else:
    grace=MultiPanelGrace(colors=ColorBrewerScheme('PRGn'))

  # dummy=[r"\| \|",r"\|\\\|",r"\|,X\|"]
  dummy=['Herbivory','Pollination','','','','']
  # dummy=['Total overlap','Partial overlap','No overlap','','','']


  grace.add_label_scheme("dummy",dummy)
  grace.set_label_scheme("dummy")

  lineplotter(grace,datapath,modeltype,colormode)
  print 'plots made'

  grace.multi(rows=2,cols=1,hgap=.05,vgap=.04)
  # grace.automulti()
  grace.hide_redundant_labels()
  # grace.set_col_yaxislabel(col=0,rowspan=(0,1),label='Probability of sharing partners',place='normal',just=2,char_size=1,perpendicular_offset=0.06)
  # grace.hide_redundant_labels()


  grace.set_row_xaxislabel(row=1,colspan=(None,None),label='Phylogenetic distance (My)',place='normal',just=2,char_size=1,perpendicular_offset=0.06)
  grace.write_file('../../manuscript/Figures/dataplots/scaled_regression_lines_'+graphtype+'_'+colormode+'.eps')




if __name__ == '__main__':
  main()
