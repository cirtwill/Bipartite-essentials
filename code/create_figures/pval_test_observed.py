def pval_getter(netdir):
  Jaccard_pvals=[]
  Sorenson_pvals=[]
  for file in netdir:
    f=open(file,'r')
    for line in f: 



def main():

  bigdir='../../data/Jaccard/Observed_Regression/'
  grace=MultiPanelGrace(colors='RdBu')

  for nettype in os.listdir(bigdir):
    for network in os.listdir(bigdir+nettype+'/'):
      graph=grace.add_graph(Panel)    

      pvals=pval_getter(bigdir+nettype+'/'+network)


  grace.multi(rows=10,cols=7,vgap=.03,hgap=.03)



if __name__ == '__main__':
  main()
