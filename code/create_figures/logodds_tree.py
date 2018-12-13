import os
import sys
from user import pygracePackagePath
sys.path.append(pygracePackagePath)

from math import log, fabs

from PyGrace.grace import Grace
from PyGrace.colors import ColorBrewerScheme
from PyGrace.drawing_objects import DrawText
from PyGrace.Extensions.panel import MultiPanelGrace,Panel,TreePanel
from PyGrace.Extensions.colorbar import ColorBar
from PyGrace.axis import LINEAR_SCALE, LOGARITHMIC_SCALE

# ---------------------------------- functions to read the data

def read_species_data(filename,web):
    inFile = open(filename,'r')
    inFile.readline()
    data = inFile.readlines()
    inFile.close()

    species_data = {}
    for line in data:
        sline = line.strip().split(',')
        if sline[0] == web:
            n_prey = int(sline[11])
            g_predator = float(sline[13])
            z_predator = float(sline[15])
            species_data[sline[-1]] = [n_prey, g_predator, z_predator]

    return species_data

def read_tree(filename):
    inFile = open(filename,'r')
    data = inFile.readline()
    inFile.close()
    return data

# ---------------------------------- this is the part where YOU do the analysis

# make a Grace instance with the "Set1" color scheme
colors = ColorBrewerScheme("Greys",n=253) # this is the maximum number of colors
colors = ColorBrewerScheme("Greens",n=253) # this is the maximum number of colors
grace = MultiPanelGrace(colors=colors)#ColorBrewerScheme('Paired'))
grace.set_label_scheme("latin",)

# create graphs and set locations on page
graph1 = grace.add_graph(TreePanel,orientation='down')
graph2 = grace.add_graph(Panel,)#type="chart",)
#graph3 = grace.add_graph(Panel,)#type="chart",)
graph4 = grace.add_graph(Panel,)#type="chart",)

web = 'Caricaie_Lakes'

tree = graph1.add_tree(read_tree('../../../data/'+web+'/Calculations/tree.newick'))
tip_labels = dict(zip([i.replace(" ","_") for i in graph1.xaxis.tick.spec_ticklabels],
                      graph1.xaxis.tick.spec_ticks))

species_data = read_species_data('../../../data/species_specific_statistics.dat',web)
n_prey_data = []
g_predator_data = []
z_predator_data = []
for s in tip_labels:
    x = tip_labels[s]
    n_prey_data.append([x,species_data[s][0]])
    g_predator_data.append([x,species_data[s][1]])
    z_predator_data.append([x,-species_data[s][2]])

# we will have one dataset for each bar
# that way we can use different colors for each depending on the size






bars = []
for graph, dataset in [ [graph2, n_prey_data],
                        #[graph3, g_predator_data],
                        [graph4, z_predator_data],
                        #[graph4, z_predator_data],
                      ]:
  # create a false colorbar
  zmin = min([fabs(i[-1]) for i in dataset])
  zmax = max([fabs(i[-1]) for i in dataset])
  zmin = zmin - (zmax-zmin)
  colorbar = Grace(colors=colors).add_graph(ColorBar,domain=(zmin,zmax),
                                            scale=LINEAR_SCALE,autoscale=False)

  for i in dataset:
    if i[1] != 0:
      color = colorbar.z2color(zmin+(zmax-fabs(i[-1])))#i[-1])
      #color = colorbar.z2color(fabs(i[-1]))
      data = [i]
      bars.append(graph.add_dataset(data, type='bar', color=color))
      bars[-1].symbol.configure(linestyle=0, linewidth=0, fill_color=color,)
      bars[-1].line.configure(linestyle=0, linewidth=0, color=color)

# arrange the graphs as fit and autoformat based upon size
grace.multi(4,1,vgap=0.07,width_to_height_ratio=6,)#hgap=0.10,)
#graph1.autoscale()
grace.autoformat()

# make the tree's lines thicker
tree.line.configure(linewidth=1.25,)

# adjust the width of the bars
for bar in bars:
    bar.symbol.configure(size=0.20,)

# for all graphs...
for graph in grace.graphs:
    # scale the size of the ticks by a factor of 0.6
    graph.xaxis.tick.scale_suffix(0.6, 'size', all=True)
    graph.yaxis.tick.scale_suffix(0.6, 'size', all=True)

    # adjust the tick labels
    graph.xaxis.tick.configure(major=10,minor_ticks=1,place_rounded='true',)
    graph.xaxis.ticklabel.configure(format="decimal",char_size=1.0,offset_tup=(0.00,0.015),)
    graph.yaxis.tick.configure(minor_ticks=1,place_rounded='true')
    graph.yaxis.ticklabel.configure(format="decimal",char_size=1.0,)#offset_tup=(0.00,0.01))

    # adjust the location of the panel labels
    graph.panel_label.configure(dx=0.025,dy=-0.04,placement="iur",)
 
    #graph.xaxis.configure(offset=(-0.07,0.0))

# adjust the bounds for panels a and b
xmin = min(tip_labels.values())
xmax = max(tip_labels.values())

# data = [[xmin-5,0],[xmax+5,0]]
# data = [[xmin,0],[xmax,0]]
# hline = graph4.add_dataset(data, type='xy')
# hline.symbol.configure(shape=0,)
# hline.line.configure(linewidth=1.35320133245,linestyle=3,)

for graph in grace.graphs:
    graph.world.xmin = xmin-5
    graph.world.xmax = xmax+3

# get rid of the tick labels for panel a
graph1.xaxis.configure(onoff='off',)

# adjust the axes for panels b and c
#for graph in [graph2, graph3, graph4]:
for graph in [graph2, graph4]:
    graph.frame.configure(type=1,linewidth=1)
    graph.xaxis.configure(onoff='off',)
    graph.xaxis.tick.configure(onoff='off',)#major=1,minor_ticks=0,place='normal',)
    graph.xaxis.ticklabel.configure(onoff='off',)
    graph.yaxis.tick.configure(place='normal',)
    graph.yaxis.bar.configure(onoff='off',)

graph2.yaxis.tick.configure(major=100)
graph3.yaxis.tick.configure(major=100)
graph4.yaxis.tick.configure(major=50)

graph2.world.ymin = 150
graph2.world.ymax = -200

graph3.world.ymin = 125
graph3.world.ymax = -50

graph4.world.ymin = 
graph4.world.ymax = 10

# add pseudo axis labels
# doing it like this makes certain that all are aligned together
# for graph, text in [
#                     [graph2, 'Number of prey'],
#                     #[graph3, 'Absolute intervality'],
#                     [graph4, 'Relative intervality'],
#                    ]:

#     coords = graph.get_view()
#     graph.add_drawing_object(DrawText, text=text,
#                              x=coords[0]-0.06,
#                              y=coords[1] + (coords[3]-coords[1])/2.0,
#                              just=2, char_size = 0.90, rot=90,)

# graph4.add_drawing_object(DrawText, text='Species',
#                           x=coords[0] + (coords[2]-coords[0])/2.0,
#                           y=coords[1] - 0.03,
#                           just=2, char_size = 0.90,)


# sets everything to Helvetica except the titles, which are Bigger and Bolder
grace.set_fonts('Helvetica')
grace.configure_group(graph1.panel_label,
                      graph2.panel_label,
                      #graph3.panel_label,
                      graph4.panel_label,
                      font='Helvetica-Bold', char_size=1.25,)# rot=270)

grace.configure_group(graph2.yaxis.label,
                      #graph3.yaxis.label,
                      graph4.xaxis.label,
                      graph4.yaxis.label,
                      char_size=0.90,)# rot=270)

# print the grace (.agr format) to a file
#grace.write_file('phylogenetic_signal.agr')

# print the grace (.eps format) to a file
grace.write_file('../../manuscript/Figures/dataplots/family_signal_tree.eps')
