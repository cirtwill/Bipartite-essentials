import sys 
import os 
import re 
import random 
from decimal import *
import math

from PyGrace.grace import Grace
from PyGrace.colors import RandomColorScheme, MarkovChainColorScheme, ColorBrewerScheme
from PyGrace.dataset import SYMBOLS
from PyGrace.Extensions.panel import Panel,MultiPanelGrace, TreePanel
from PyGrace.drawing_objects import DrawText, DrawLine

from PyGrace.Extensions.distribution import CDFGraph, PDFGraph
from PyGrace.Extensions.latex_string import LatexString, CONVERT

# Update the scale dict, update the scales for each plot.
scaledict={
  "adoxaceae":(109.005904,72.33798048),
  "amaranthaceae_ph":(63.31440233,25.6747469),
  "amaryllidaceae":(124.3113023,23.22845123),
  "apiaceae":(97.08918062,49.51149577),
  "apocynaceae":(67.32058251,19.57696024),
  "araliaceae_ph":(99.42261375,29.52333939),
  "asparagaceae":(126.7490068,34.97861194),
  "asteraceae_pp":(80.27592,20.89695),
  "asteraceae_ph":(81.03086142,22.84774091),
  "berberidaceae":(170.1549313,111.5126936),
  "boraginaceae":(104.3294132,19.93357802),
  "brassicaceae":(86.85651906,50.0135176),
  "cactaceae_ph":(29.48932,11.53711841),
  "calceolariaceae":(39.951931,14.58840519),
  "campanulaceae":(88.27866667,30.58062718),
  "caprifoliaceae":(123.2603062,25.03345494),
  "caryophyllaceae":(81.10386123,32.17269234),
  "cistaceae":(54.06062086,25.37135909),
  "convolvulaceae":(74.26640822,42.3053962),
  "cornaceae_ph":(113.032486,39.81259219),
  "ericaceae":(90.05900849,36.05961842),
  "euphorbiaceae":(172.4392253,43.00556316),
  "fabaceae_pp":(101.9271,43.96578),
  "fabaceae_ph":(85.61470337,40.71417068),
  "gentianaceae_ph":(37.2132315,31.22748797),
  "geraniaceae":(61.21654733,29.18579945),
  "hydrangeaceae":(101.5381486,26.70867942),
  "iridaceae":(126.447704,42.84244667),
  "lamiaceae":(50.14136334,20.88719942),
  "lauraceae":(156.3378,48.7914293),
  "liliaceae_ph":(103.9309355,25.930929),
  "loasaceae":(94.21335667,61.85765685),
  "malpighiaceae":(132.7640406,24.81478486),
  "malvaceae":(119.511597,40.09529051),
  "melastomataceae_pp":(106.7518,28.64504),
  "melastomataceae_ph":(113.9874286,18.0004521),
  "montiaceae":(36.3959764,10.34172023),
  "moraceae":(78.6853888,42.22114964),
  "myrtaceae":(103.0648759,56.8557266),
  "nothofagaceae":(56.97537133,45.3545379),
  "oleaceae":(32.1162688,11.81411572),
  "onagraceae":(100.7243267,42.12984757),
  "orchidaceae":(215.9082096,27.04037122),
  "orobanchaceae":(47.08907933,28.17367719),
  "oxalidaceae_ph":(68.64646367,24.19685417),
  "papaveraceae":(202.1400649,47.3636299),
  "phyllanthaceae":(180.252555,40.13878657),
  "pinaceae":(332.08031,144.0379999),
  "plantaginaceae":(42.39444459,23.33636822),
  "poaceae_pp":(32.33723,6.241072),
  "poaceae_ph":(61.97905111,40.73114384),
  "polygonaceae":(85.93899135,34.11069847),
  "primulaceae":(82.25106947,34.74681284),
  "ranunculaceae":(174.9632676,56.19255598),
  "rhamnaceae_ph":(173.0373568,41.35478483),
  "rosaceae":(146.7963622,37.15767631),
  "rubiaceae_pp":(104.7472,17.45647),
  "rubiaceae_ph":(72.73950725,40.77162894),
  "salicaceae":(11.11558467,5.422243654),
  "sapindaceae_pp":(90.11804,73.40842),
  "sapindaceae_ph":(125.8753868,20.95015513),
  "saxifragaceae":(88.9375448,53.93318612),
  "solanaceae":(60.82260943,39.62169044),
  "tropaeolaceae":(60.11397333,19.70532409),
  "verbenaceae":(26.21984517,26.58451036),
  "violaceae":(53.95708522,49.00825072),
  "zingiberaceae_ph":(145.553092,41.58659467),
  "overall":(92.11035845,42.69432146)}


# Two families didn't converge (small samples with one odd value)
non_convergent={'pp':'lauraceae','ph':'sapindaceae'}

def read_tree(filename):
    inFile = open(filename,'r')
    data = inFile.readline()
    inFile.close()
    return data

def signalreader(datapath,family,nettype):
  databank={'fixef':{},'ranef':{}}
  try:
    f=open(datapath+family+'_'+nettype+'_reg_fixef.tsv','r')
    for line in f:
      if line.split()[0]!='"Estimate"':
        name=line.split()[0][1:-1]
        effect=float(line.split()[1])
        SE=float(line.split()[2])
        p=float(line.split()[4])
        databank['fixef'][name]=(effect,SE,p)
    f.close()
  except IOError:
    databank={'fixef':{},'ranef':{}}
  return databank

def overall_signalreader(datafile):
  databank={}
  f=open(datafile,'r')
  for line in f:
    if line.split()[0]!='"Estimate"':
      name=line.split()[0][1:-1]
      effect=float(line.split()[1])
      databank[name]=effect
  f.close()
  phslope=databank['scale(distance)']*scaledict['overall'][1]
  ppslope=(databank['scale(distance)']+databank['scale(distance):nettypepp'])*scaledict['overall'][1]

  return phslope, ppslope

def lineplotter(datapath,family,grace,graph,x,graphtype,supertype,nettype,summarydict):
  databank=signalreader(datapath,family,nettype)
  if family not in non_convergent[nettype] and databank!={'fixef':{},'ranef':{}}:
    try:
      scal=scaledict[family]
    except KeyError:
      scal=scaledict[family+'_'+nettype]
    y=databank['fixef']['scale(distance)'][0]*scal[1]
    err=databank['fixef']['scale(distance)'][1]*scal[1]*1.96
    p=databank['fixef']['scale(distance)'][2]
    summarydict[family][nettype]=(str(x),str(p))
    if nettype=='ph' and family in ['rubiaceae']:
      x=x+.25
    if y>0:
      if y-err >0:
        sig=1
      else:
        sig=0
    elif y<0:
      if y+err <0:
        sig=1
      else:
        sig=0
    else:
      print family
    if sig==1:
      dat=graph.add_dataset([(x,y,err)],type='xydy')
      if graphtype=='grey':
        if nettype=='pp':
          col=8
        else:
          col=5
      else:
        if nettype=='pp':
          col=3
        else:
          col=10

      dat.symbol.configure(color=1,fill_color=col,size=.6,linewidth=.3,shape=3)
      dat.line.linestyle=0
      dat.errorbar.configure(riser_linewidth=1,linewidth=1.25,size=.75)

      if y>150:
        graph.add_drawing_object(DrawLine,arrow=2,start=(60,y),end=(85,y),loctype='world')
        # if y-err > 0:
        #   graph.add_drawing_object(DrawText,text='*',x=x,y=60,just=2,loctype='world')

      if y< -100:
        graph.add_drawing_object(DrawLine,arrow=2,start=(-60,y),end=(-85,y),loctype='world')

        # if y+err < 0:
        #   graph.add_drawing_object(DrawText,text='*',x=x,y=-65,just=2,loctype='world')

  return graph, summarydict

def overall_lineplotter(graph,grace,supertype,graphtype):
  datafile='../../data/Jaccard/Observed_regression/overall_bynetwork_reg_unranked_scaled_fixef.tsv'

  phslope, ppslope=overall_signalreader(datafile)

  if graphtype=='grey':
    col1=5
    col2=8
  else:
    col1=10
    col2=3

  if supertype=='paper':
    Hline=graph.add_dataset([(0,phslope),(60,phslope)])
    Hline.symbol.size=0
    Hline.line.configure(linewidth=1.25,color=col1)

  # print phslope, ppslope
  Pline=graph.add_dataset([(0,ppslope),(60,ppslope)])
  Pline.symbol.size=0
  Pline.line.configure(linewidth=1.25,linestyle=1,color=col2)

  return graph

def main():

  datapath='../../data/Jaccard/families_to_networks/Regressions/'

  summarydict={}
  families=['adoxaceae','amaryllidaceae','apiaceae','apocynaceae','asparagaceae','asteraceae','berberidaceae','boraginaceae','brassicaceae','calceolariaceae','campanulaceae','caprifoliaceae','caryophyllaceae','cistaceae','convolvulaceae','ericaceae','euphorbiaceae','fabaceae','geraniaceae','hydrangeaceae','iridaceae','lamiaceae','loasaceae','malpighiaceae','malvaceae','melastomataceae','montiaceae','moraceae','myrtaceae','nothofagaceae','oleaceae','onagraceae','orchidaceae','orobanchaceae','papaveraceae','phyllanthaceae',
            'pinaceae','plantaginaceae','poaceae','polygonaceae','primulaceae','ranunculaceae','rosaceae','rubiaceae','salicaceae','sapindaceae','saxifragaceae','solanaceae','tropaeolaceae','verbenaceae','violaceae']

  # # It appears we are only plotting significant families. This brings us down to 15 instead of 51, so good plan.
  # sig_families=['apiaceae','apocynaceae','asteraceae','boraginaceae','cistaceae','euphorbiaceae'
  #               ,'fabaceae','lamiaceae','melastomataceae','plantaginaceae','poaceae','polygonaceae','ranunculaceae','rubiaceae']
  # In order following the tree:
  sig_families=['poaceae','fabaceae','euphorbiaceae','melastomataceae','cistaceae','polygonaceae',
        'lamiaceae','plantaginaceae','rubiaceae','amaryllidaceae','boraginaceae','apiaceae','asteraceae',
        'ranunculaceae']


# # The only ones with two...
# asteraceae_ph_reg_fixef.tsv
# asteraceae_pp_reg_fixef.tsv
# fabaceae_ph_reg_fixef.tsv
# fabaceae_pp_reg_fixef.tsv
# melastomataceae_ph_reg_fixef.tsv
# melastomataceae_pp_reg_fixef.tsv
# poaceae_ph_reg_fixef.tsv
# poaceae_pp_reg_fixef.tsv
# rubiaceae_ph_reg_fixef.tsv
# rubiaceae_pp_reg_fixef.tsv


  grace=MultiPanelGrace()
  dummy=['','','','']


  supertype='paper'
  graphtype='full'

  grace=MultiPanelGrace(colors=ColorBrewerScheme('PRGn'))

  grace.add_label_scheme("dummy",dummy)
  grace.set_label_scheme("dummy")

  graph=grace.add_graph(Panel)

  graph.world.ymin=-60
  graph.world.ymax=60
  graph.yaxis.tick.configure(place='both',major_size=.5,minor_ticks=1,minor_size=.3,major=50,major_linewidth=.5,minor_linewidth=.5)
  graph.yaxis.ticklabel.configure(char_size=.5,)
  # graph.xaxis.label.configure(text='Change in log odds',char_size=.75,just=2,place="normal")
  # graph.altxaxis.onoff='on'
  # graph.world.altxmin=-200
  # graph.world.altxmax=200
  # graph.altxaxis.bar.linewidth=.5
  # graph.altxaxis.tick.configure(place='both',major_size=.3,minor_ticks=1,minor_size=.15,major=50,major_linewidth=.5,minor_linewidth=.5)
  # graph.altxaxis.ticklabel.char_size=0
  # # graph.altxaxis.label.configure(place='opposite',text='\T{-1 0 0 -1}Partial overlap',char_size=.75,just=2)
  # graph.altxaxis.label.configure(place='opposite',text='Family',char_size=.5,just=2)

  overall_lineplotter(graph,grace,supertype,graphtype)
  print 'Overall line added'
  x=1
  for family in sig_families:
    summarydict[family]={'pp':(),'ph':()}
    for nettype in ['pp','ph']:
      lineplotter(datapath,family,grace,graph,x,graphtype,supertype,nettype,summarydict)
    x=x+1
  # graph.xaxis.ticklabel.configure(char_size=.85,format='decimal',prec=0)

  graph.frame.linewidth=.5
  graph.xaxis.bar.linewidth=.5
  graph.yaxis.bar.linewidth=.5
  
  graph.panel_label.configure(char_size=.75,placement='ouc',dy=0.01,dx=0,just=2)

  specials=graph.xaxis.tick.set_spec_ticks([1,2,3,4,5,6,7,8,9,10,11,12,13,14],[],tick_labels=sig_families)
  # specials=graph.yaxis.tick.set_spec_ticks([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,
  #  17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,
  #  44,45,46,47,48,49,50,51],[],tick_labels=families)

  graph.world.xmin=0
  graph.world.xmax=15
  graph.xaxis.tick.configure(place='both',major_size=.3,minor_ticks=0,major_linewidth=.5)
  graph.xaxis.ticklabel.configure(char_size=0,format='decimal',prec=0,angle=90,)

  # Make a tree with the significant families, re-order significant families to match tree.
  # Let's add a tree


# Forget how I got dates just now, but here is the scaffold:

# (((((((((((((((((((((((sp10)genus10)poaceae))))))poales))))))))monocots,((((((((((((((((((sp6)genus6)fabaceae))fabales),(((((((sp5)genus5)euphorbiaceae)))malpighiales)))),((((((((sp8)genus8)melastomataceae))))myrtales),(((((((((((sp4)genus4)cistaceae))))malvales)))))))))),(((((((((sp11)genus11)polygonaceae))))caryophyllales,(((((((((((((((((((((sp7)genus7)lamiaceae))))))),((sp9)genus9)plantaginaceae)))))lamiales,((((sp3)genus3)boraginaceae))boraginales)),(((sp13)genus13)rubiaceae,((((sp1)genus1)apocynaceae)))gentianales)),(((((((((((((sp)genus)apiaceae))))))apiales))),(((((((((sp2)genus2)asteraceae)))))))asterales))))))))))))),(((((((sp12)genus12)ranunculaceae)))))ranunculales)))))))));


  # graph1 = grace.add_graph(Panel)
  graph1 = grace.add_graph(TreePanel,orientation='up')
  tree = graph1.add_tree(read_tree('../../data/plant_phylogeny/dated_family_tree.new'))

  # tip_labels = dict(zip([i.replace(" ","_") for i in graph1.xaxis.tick.spec_ticklabels],
  #                 graph1.xaxis.tick.spec_ticks))      
  tree.line.configure(color=1,linewidth=1.25)

  graph1.yaxis.tick.configure(place='both',major_size=.4,minor_ticks=0,minor_size=.4,major=100,major_linewidth=1,minor_linewidth=1)
  graph1.xaxis.ticklabel.configure(char_size=.5,format='decimal',prec=0,angle=90)
  graph1.autoscale()
  graph1.world.xmin=0
  graph1.world.xmax=52

  grace.multi(rows=2,cols=1,hgap=.09,vgap=.03,width_to_height_ratio=1/.33)
  view = grace.graphs[1].get_view()

  grace.graphs[0].yaxis.label.configure(text='Change in log odds (My\S-1\N)',place='normal',just=2,char_size=1,place_tup=(0, 0),)
  grace.graphs[0].set_view(.25,.65,.75,.95)
  grace.graphs[1].set_view(.25,.3,2,.52)

  grace.write_file('../../manuscript/Figures/dataplots/Family/allfams_'+graphtype+'.eps')



  # # And now Alyssa saves herself a lot of work un-scaling the values by hand.
  # g=open('../../data/Regressions/family_summarytable_data.tsv','w')
  # g.write('family\tnettype\tX1\tXp\tN1\tNp\tll1\tllp\n')
  # for family in sorted(summarydict):
  #   if summarydict[family]['ph']!={'X':(),'N':(),'ll':()}:
  #     g.write(family+'\tph\t')
  #     # All the PH ones worked for all three patterns      
  #     g.write('\t'.join(summarydict[family]['ph']['X'])+'\t')
  #     g.write('\t'.join(summarydict[family]['ph']['N'])+'\t')
  #     g.write('\t'.join(summarydict[family]['ph']['ll'])+'\n')

  # for family in sorted(summarydict):
  #   if summarydict[family]['pp']!={'X':(),'N':(),'ll':()}:
  #     g.write(family+'\tpp\t')
  #     if summarydict[family]['pp']['X']!=():
  #       g.write('\t'.join(summarydict[family]['pp']['X'])+'\t')
  #     else:
  #       g.write('-\t-\t')
  #     if summarydict[family]['pp']['N']!=():
  #       g.write('\t'.join(summarydict[family]['pp']['N'])+'\t')
  #     else:
  #       g.write('-\t-\t')
  #     if summarydict[family]['pp']['ll']!=():
  #       g.write('\t'.join(summarydict[family]['pp']['ll'])+'\n')    
  #     else:
  #       g.write('-\t-\n')
  # g.close()


if __name__ == '__main__':
  main()

