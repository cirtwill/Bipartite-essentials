import os
import sys
import numpy as np

from PyGrace.grace import Grace
from PyGrace.colors import RandomColorScheme, MarkovChainColorScheme, ColorBrewerScheme
from PyGrace.dataset import SYMBOLS
from PyGrace.Extensions.panel import Panel,MultiPanelGrace, TreePanel
from PyGrace.drawing_objects import DrawText, DrawLine

from PyGrace.Extensions.distribution import CDFGraph, PDFGraph
from PyGrace.Extensions.latex_string import LatexString, CONVERT


def pval_reader(pfile):
	pvals={}
	f=open(pfile,'r')
	for line in f:
		if line.split()[0]!='"V1"':
			network=line.split()[0]
			ps=line.split()[1:]
			pvals[network]=[float(x) for x in ps]
	f.close()
	return pvals

def pval_binner(ps):
	bins={}
	used=[]
	for i in range(0,21):
		binmin=round(i*0.05,2)
		binmax=round(binmin+0.05,2)
		binmed=round(np.mean([binmin,binmax]),3)
		bins[binmed]=[]
		for x in sorted(ps):
			if round(x,3)>=binmin and round(x,3)<binmax:
				bins[binmed].append(x)
				used.append(x)
		lesser=[x for x in ps if x<binmax]
		greater=[x for x in lesser if x>=binmin]
		bins[binmed]=greater
	lens=[]
	total=0
	for x in sorted(bins):
		y=len(bins[x])
		lens.append((x-0.025,float(y)/999))
		lens.append((x+0.025,float(y)/999))
		total=total+y

	if total!=len(ps):
		print [x for x in ps if x not in used], 'unused'
		print total, len(ps), 'error in binning'
		sys.exit()
	return lens

def format_graph(graph):
  graph.world.xmin=0
  graph.world.xmax=1
  graph.xaxis.tick.configure(major=.2,minor_ticks=0,major_size=.5,major_linewidth=.5)
  graph.xaxis.ticklabel.char_size=0.5

  graph.world.ymax=.08
  graph.yaxis.tick.configure(major=.02,minor_ticks=0,major_size=.5,major_linewidth=.5)
  graph.yaxis.ticklabel.char_size=0.5

  graph.frame.linewidth=.5
  graph.xaxis.bar.linewidth=.5
  graph.yaxis.bar.linewidth=.5

  graph.panel_label.configure(char_size=.5,placement='iul',dy=0.02,dx=0.02,just=2)

  return graph

def format_dummy(graph):
  graph.xaxis.tick.configure(major_linestyle=0)
  graph.xaxis.ticklabel.char_size=0
  graph.yaxis.tick.configure(major_linestyle=0)
  graph.yaxis.ticklabel.char_size=0

  graph.frame.configure(linewidth=0,linestyle=0)
  graph.xaxis.bar.configure(linewidth=0,linestyle=0)
  graph.yaxis.bar.linestyle=0

  graph.panel_label.configure(char_size=0,placement='iul',dy=0.02,dx=0.02,just=2)

  return graph
 
def populate_graph(graph,dats,key,j):
	if 'ph' in key:
		col=12-j
	else:
		col=2+j
 	dataset=graph.add_dataset(dats)
 	dataset.line.configure(linewidth=.5,color=col)
 	dataset.symbol.shape=0

 	return graph

def main():

  pfile='../../data/Jaccard/Observed_Regression/random_vs_randomrandom.tsv'
  pvals=pval_reader(pfile)
  binned_pvals={}
  for net in pvals:
  	binned_pvals[net]=pval_binner(pvals[net])

  pps=[x for x in pvals.keys() if 'M_PL' in x]
  phs=[x for x in pvals.keys() if 'ph' in x]

  # bigdir='../../data/Jaccard/Observed_Regression/'
  grace=MultiPanelGrace(colors=ColorBrewerScheme('PRGn'))

  # grace.add_label_scheme("dummy",dummy)
  # grace.set_label_scheme("dummy")
  for i in range(0,12):
  	keys=sorted(pps)[i*5:i*5+5]
  	print i, len(keys)
	graph=grace.add_graph(Panel)
	graph=format_graph(graph)
	j=0
	for key in keys:
		graph=populate_graph(graph,binned_pvals[key],key,j)
		j=j+1
  for i in range(0,3):
  	keys=sorted(phs)[i*5:i*5+5]
  	if i==1:
  		keys.append(sorted(phs)[-1])
  	elif i==2:
  		keys=[]
  	print i,len(keys)
	graph=grace.add_graph(Panel)
	graph=format_graph(graph)
	j=0
	for key in keys:
		graph=populate_graph(graph,binned_pvals[key],key,j)
		j=j+1  

  grace.multi(rows=5,cols=3,hgap=.02,vgap=.02)
  grace.hide_redundant_labels()
  grace.graphs[14]=format_dummy(graph)

  grace.set_col_yaxislabel(col=0,rowspan=(None,None),label='Frequency',char_size=.75,just=2,perpendicular_offset=0.07)  
  grace.set_row_xaxislabel(row=4,colspan=(None,None),label='Probability',char_size=.75,just=2,perpendicular_offset=0.05)
  grace.write_file('../../manuscript/Figures/random_p_distributions.eps')



if __name__ == '__main__':
  main()
