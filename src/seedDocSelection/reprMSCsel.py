import os
import re
import sys
import random
import jsonlines
import dill as pickle
from scipy.stats import t
from collections import defaultdict, OrderedDict

def combineMSCwiseAll(mscwiseTxtDir):
	"""
	Input: Folder location with disciplines (separate folder for each discipline) 
	and their documents.
	Output: Freq of tokens in each MSC
	"""
	lstDir = os.listdir(mscwiseTxtDir)
	mscAlltxt = defaultdict(lambda:0)

	for dir1 in lstDir:
		print("working on directory: ",dir1)
		with open(mscwiseTxtDir+"/"+dir1, 'rb') as fz:
			mscindfreq = pickle.load(fz)
		
		for keyI in mscindfreq[list(mscindfreq.keys())[0]]:
			mscAlltxt[keyI] += mscindfreq[list(mscindfreq.keys())[0]][keyI]

	with open("mscWiseTextAll.pkl", 'wb') as fz:
		pickle.dump(mscAlltxt, fz)


def tokensCoverage(mscwiseTxtDir):
	"""
	Input: Folder location with disciplines (separate folder for each discipline) 
	and their documents.
	Output: Tokens coverage T_c estimate.
	"""
	with open("mscWiseTextAll.pkl", 'rb') as fz:
		mscAll = pickle.load(fz)
	mscAllsort = OrderedDict(sorted(mscAll.items(), key=lambda kv: kv[1], reverse=True))
	mscAllsort = {ke: va for ke, va in mscAllsort.items() if len(ke) > 3}
	refToksmscAll = set(list(mscAllsort.keys())[:1000])

	lstDir = os.listdir(mscwiseTxtDir)
	mscAlltxt = defaultdict(lambda:0)

	for dir1 in lstDir:
		with open(mscwiseTxtDir+"/"+dir1, 'rb') as fz:
			mscindfreq = pickle.load(fz)
		mscIndsort = OrderedDict(sorted(mscindfreq[list(mscindfreq.keys())[0]].items(), key=lambda kv: kv[1], reverse=True))
		mscIndsort = {ke: va for ke, va in mscIndsort.items() if len(ke) > 3}
		refToksmscInd = set(list(mscIndsort.keys())[:1000])
		percTokcov = (len(refToksmscInd.intersection(refToksmscAll))/len(refToksmscAll))*100
		print("working on directory: ",dir1, percTokcov)


def checkAllcombToks():
	with open("mscWiseTextAll.pkl", 'rb') as fz:
		mscAll = pickle.load(fz)
	mscAllsort = OrderedDict(sorted(mscAll.items(), key=lambda kv: kv[1], reverse=True))
	mscAllsort = {ke: va for ke, va in mscAllsort.items() if len(ke) > 3}
	print(list(mscAllsort.keys())[:10])


def spearmanCorrrow(mscwiseTxtDir):
	"""
	Input: Folder location with disciplines (separate folder for each discipline) 
	and their documents.
	Output: Spearman correlation coeffiecient estimate along with
	p-values.
	"""
	with open("mscWiseTextAll.pkl", 'rb') as fz:
		mscAll = pickle.load(fz)
	mscAllsort = OrderedDict(sorted(mscAll.items(), key=lambda kv: kv[1], reverse=True))
	mscAllsort = {ke: va for ke, va in mscAllsort.items() if len(ke) > 3}

	refToksmscAll = dict()	
	i =0
	for valH in mscAllsort.keys():
		i += 1
		if i > 1000:
			break
		refToksmscAll[valH] = mscAllsort[valH]
	refRanks = list(refToksmscAll.values())

	lstDir = os.listdir(mscwiseTxtDir)
	mscAlltxt = defaultdict(lambda:0)

	for dir1 in lstDir:
		with open(mscwiseTxtDir+"/"+dir1, 'rb') as fz:
			mscindfreq = pickle.load(fz)
		mscIndsort = OrderedDict(sorted(mscindfreq[list(mscindfreq.keys())[0]].items(), key=lambda kv: kv[1], reverse=True))
		mscIndsort = {ke: va for ke, va in mscIndsort.items() if len(ke) > 3}

		refToksMSCindiv = dict()
		for keyComb in refToksmscAll.keys():
			if keyComb in mscIndsort:
				refToksMSCindiv[keyComb] = mscIndsort[keyComb]

		refToksMSCindiv = OrderedDict(sorted(refToksMSCindiv.items(), key=lambda kv: kv[1], reverse=True))
		differSumm = 0
		j = 0
		for keyComb in refToksmscAll.keys():
			if keyComb in list(refToksMSCindiv.keys()):
				j += 1
				differSumm += (j - list(refToksMSCindiv.keys()).index(keyComb)) ** 2
		#print(spearmanCoe)
		try:
			spearmanCoe = 1 - ((6*differSumm)/(len(refToksMSCindiv)* (len(refToksMSCindiv)**2-1)))
			tRef = spearmanCoe * (((len(refToksMSCindiv) - 2)/(1 - (spearmanCoe**2))) ** 0.5)
			pVal = 1 - t.cdf(x=tRef, df=len(refToksMSCindiv)-2)
			print("Spearman Coe on MSC: ",dir1, len(refToksMSCindiv), spearmanCoe, pVal)	
		except:
			print("Spearman Coe on MSC: ",dir1, len(refToksMSCindiv),  spearmanCoe, "lolNothing")



#checkAllcombToks()
#combineMSCwiseAll()
#tokensCoverage()
#spearmanCorrrow()