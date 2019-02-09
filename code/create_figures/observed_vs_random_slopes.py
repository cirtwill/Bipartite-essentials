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


def read_regfile(regfile):
  obslopes={'pp':[],'ph':[]}
  ranslopes={'pp':[],'ph':[]}
  f=open(regfile,'r')
  for line in f:
    if line.split()[0]!='"Observed"':
      netname=line.split()[0][1:-1]
      if netname[:2]=='ph':
        nettype='ph'
      elif netname[:4]=='M_PL':
        nettype='pp'
      if nettype not in ['pp','ph']:
        print line.split()[:3]
        sys.exit()
      obs=float(line.split()[1])
      rans=line.split()[2:]
      obslopes[nettype].append(obs)
      for ran in rans:
        ranslopes[nettype].append(float(ran))
  f.close()

  return obslopes, ranslopes

def format_graph(graph,nettype):

  graph.world.ymin=-.600000000001
  graph.world.ymax=.2
  graph.yaxis.tick.configure(place='both',major_size=.4,minor_ticks=1,minor_size=.2,major=.2,major_linewidth=1,minor_linewidth=1)
  graph.yaxis.ticklabel.configure(char_size=.75,format='decimal',prec=1)
  graph.yaxis.bar.linewidth=1

  graph.world.xmin=0.45
  graph.world.xmax=.55
  graph.xaxis.tick.configure(place='both',major_size=.4,minor_ticks=1,minor_size=.2,major=2,major_linewidth=1,minor_linewidth=1)
  graph.xaxis.ticklabel.configure(char_size=0,format='decimal',prec=0)

  graph.frame.linewidth=1
  graph.xaxis.bar.linewidth=1
  
  graph.panel_label.configure(char_size=.85,placement='ouc',dy=0.01,dx=0,just=2)

  return graph

def grace_setup(obsslopes,ranslopes):
  # dummy=[r"\| \|",r"\|\\\|",r"\|,X\|"]
  dummy=['PH','PP','','','','']
  # dummy=['Total overlap','Partial overlap','No overlap','','','']
  grace=MultiPanelGrace(colors=ColorBrewerScheme('PRGn'))

  grace.add_label_scheme("dummy",dummy)
  grace.set_label_scheme("dummy")

  for nettype in ['ph','pp']:
    graph=grace.add_graph(Panel)
    graph=format_graph(graph,nettype)
    graph=lineplotter(graph,obsslopes[nettype],ranslopes[nettype],nettype)

  grace.multi(rows=1,cols=2,hgap=.05,vgap=.04)
  grace.hide_redundant_labels()
  # grace.hide_redundant_labels()
  grace.graphs[0].set_view(0.15,0.15,.3,.95)
  grace.graphs[1].set_view(0.32,0.15,.47,.95)
  grace.set_col_yaxislabel(col=0,rowspan=(None,None),label='Slope of regression line',place='normal',just=2,char_size=1,perpendicular_offset=0.07)

  grace.set_row_xaxislabel(row=0,colspan=(None,None),label='',place='normal',just=2,char_size=1,perpendicular_offset=0.06)
  grace.write_file('../../manuscript/Figures/dataplots/observed_vs_random.eps')


def lineplotter(graph,obs,ran,nettype):
  if nettype=='pp':
    col=3
    shap=3
  else:
    col=10
    shap=2
  obsdats=[]
  for ob in obs:
    obsdats.append((0.5,ob))
  obbo=graph.add_dataset(obsdats)
  obbo.line.linestyle=0
  obbo.symbol.configure(size=.5,shape=shap,fill_color=col,color=col)

  ranmin=sorted(ran)[0]
  ranmax=sorted(ran)[-1]

  line1=graph.add_dataset([(0,ranmax),(1,ranmax)])
  line1.symbol.shape=0
  line1.line.linewidth=.5
  line1.fill.configure(color=1,style=2,fill_pattern=2)

  line1=graph.add_dataset([(0,ranmin),(1,ranmin)])
  line1.symbol.shape=0
  line1.line.linewidth=.5
  line1.fill.configure(color=1,style=2,fill_pattern=2)
  print ranmin,ranmax


    # for network in databank['ranef']:
    #   subfolder=network.split('-')[0].split('/')[0]
    #   if subfolder=='Stouffer_Ecology_Matrices':
    #     nettype='pp'
    #   else:
    #     nettype='ph'

    #   if nettype==rowtype:
    #     if nettype=='pp':
    #       inter=ppinter+databank['ranef'][network][0]
    #       beta=ppbeta+databank['ranef'][network][1]
    #       if modeltype=='ranked':
    #         data=simlines(inter,beta)
    #       else:
    #         data=simlines_scaled(inter,beta)

    #       dat=graph.add_dataset(data)
    #       dat.symbol.shape=0
    #       if colormode=='grey':
    #         dat.line.configure(linestyle=1,linewidth=1,color=6)
    #       else:
    #         dat.line.configure(linestyle=1,linewidth=1,color=4)

    #     else:
    #       inter=phinter+databank['ranef'][network][0]
    #       beta=phbeta+databank['ranef'][network][1]
    #       if modeltype=='ranked':
    #         data=simlines(inter,beta)
    #       else:
    #         data=simlines_scaled(inter,beta)

    #       dat=graph.add_dataset(data)
    #       dat.symbol.shape=0
    #       if colormode=='grey':
    #         dat.line.configure(linestyle=1,linewidth=1,color=6)
    #       else:
    #         dat.line.configure(linestyle=1,linewidth=1,color=10)

    # for dataset in [eval(rowtype+'_simdata')]:
    #   if colormode=='grey':
    #     if dataset==pp_simdata:
    #       linecol=9
    #     else:
    #       linecol=9
    #   else:
    #     if dataset==pp_simdata:
    #       linecol=2
    #     else:
    #       linecol=11
    #   dat=graph.add_dataset(dataset)
    #   dat.symbol.shape=0
    #   dat.line.configure(linestyle=1,linewidth=4,color=linecol)

  return graph

def main():

  regfile='../../data/Jaccard/Observed_Regression/observed_vs_random.tsv'

  obs,ranslopes=read_regfile(regfile)
  grace_setup(obs,ranslopes)

if __name__ == '__main__':
  main()



