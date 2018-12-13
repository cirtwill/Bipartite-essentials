import os
import sys

def random_checker(RM):
	notdone=[]
	ranwebs=os.listdir(RM)
	for web in sorted(ranwebs):
		n_random=len(os.listdir(RM+'/'+web))
		if n_random!=999:
			print web, 999-n_random, "randomisations to go"
			notdone.append(web)
	return notdone

def doubleran_checker(RRM,notdone):
	orig=os.listdir(RRM)
	for web in orig:
		if web not in notdone:
			ranwebs=os.listdir(RRM+'/'+web)
			# if len(ranwebs)!=999:
			# 	print web, len(ranwebs), 'missing a few head folders'
			for rando in ranwebs:
				dubs=os.listdir(RRM+'/'+web+'/'+rando)
				if len(dubs)!=500:
					print web, rando, len(dubs), 'missing double randomisations'

def counter_checker(JD):
	dirs=sorted(os.listdir(JD))
	if len(dirs)<70:
		print 'not all webs are done yet'
	else:
		print 'all webs present and accounted for'
	for dire in dirs:
		if dire!='.gitattributes' and '.zip' not in dire:
			if len(os.listdir(JD+'/'+dire))!=3*999:
				dones=set()
				for outfile in os.listdir(JD+'/'+dire):
					if outfile!='.gitattributes':
						key=outfile.split('_')[-2]
						dones.add(key)
				print len(os.listdir(JD+'/'+dire))/3, dire
				print 999-len(dones), 'to go'

def regression_checker(RD):
	files=os.listdir(RD)
	for i in range(1,60):
		outs=[]
		for fil in files:
			if 'M_PL_0'+str(i)+'_' in fil:
				outs.append(fil)
			if 'M_PL_00'+str(i)+'_' in fil:
				outs.append(fil)
		if len(outs)==2:
			print i,'done'
		else:
			print len(outs), i, 'has more or less'
	phouts=[]
	for fil in files:
		if 'ph' in fil:
			phouts.append(fil)
	if len(phouts)==22:
		print 'all phs done'
	else:
		print phouts

def main():

	RM='../data/Random_Matrices'
	RRM='../data/Random_Random_Matrices'
	JD='../data/Jaccard/Random_Matrices'
	RD='../data/Jaccard/Random_Regressions/'

	# notdone=random_checker(RM)
	# doubleran_checker(RRM,notdone)
	# counter_checker(JD)
	regression_checker(RD)

if __name__ == '__main__':
  main()


