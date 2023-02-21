import os
import re
import sys
import random
import jsonlines
import dill as pickle
from scipy.stats import t
from spacy.lang.en import English
from bs4 import BeautifulSoup
from spacy.tokenizer import Tokenizer
from scipy.stats import mannwhitneyu
from collections import defaultdict, OrderedDict, Counter


# Placeholder for data and spacy tokenizer initialization
nlp = English()
tokenizer = nlp.tokenizer
jsonDraft = {
	"docID": None,
	"reviews": None,
	"formulaeMathML": None,
	"msc": None
}

def sampleTOKsfreqtext(pathMsc14):
	"""
	Input: DOcuments from each discipline after preprocessing.
	Please note: Pickles used in the function will be created after running preprocessing
	scripts.
	Outpu: Frequncy of tokens within discipline
	"""

	with open('pckls/gutenBergToks.pkl', 'rb') as fr:
		gutenToks = pickle.load(fr)
	listOfdirs = os.listdir(pathMsc14)

	with open('mscFreDocsRevNew.pkl', 'rb') as fy:
		sampleWithfreq = pickle.load(fy)
	sampleWithfreq = OrderedDict(sorted(sampleWithfreq.items(), key=lambda kv: kv[1][0], reverse=True))

	lstwthnonsngleIDS = dict()
	for key in sampleWithfreq.keys():
		if sampleWithfreq[key][0] != 1:
			rvisedLst = list(set(sampleWithfreq[key][1]))
			lstwthnonsngleIDS[key] = [len(rvisedLst), rvisedLst]

	totalCorp = list()
	for idH in lstwthnonsngleIDS.keys():
		totalCorp = totalCorp + lstwthnonsngleIDS[idH][1]

	randSamplecorp = defaultdict(lambda:list())
	for sampleID in range(0,100):
		listofIDS = list()
		for key_each in list(lstwthnonsngleIDS.keys()):
			listofIDS.append(random.choice(lstwthnonsngleIDS[key_each][1]))
		randSamplecorp[sampleID] = listofIDS
	
	with open("randSamplecorp.pkl", 'wb') as fe:
		pickle.dump(randSamplecorp, fe)

	cmbndLstTxtTokfreq = defaultdict(lambda:0)
	cmbndLstMthTokfreq = defaultdict(lambda:0)
	rndmSmpsTxtTokfreq = defaultdict(lambda:defaultdict(lambda:0))
	rndmSmpsMthTokfreq = defaultdict(lambda:defaultdict(lambda:0))

	for dir1 in listOfdirs:
		print("working with directory: ",dir1)
		with jsonlines.open(pathMsc14+"/"+dir1) as reader:
			for obj in reader:
				if obj["docID"] in totalCorp:
					tokensRev = defaultdict(lambda:0)
					ohneMath = re.sub(r'\\\(.+?\\\)', '', obj["reviews"])
					ohneSpeMen = re.sub(r'\[.+?\]', '',ohneMath)
					rmSPace = ' '.join(ohneSpeMen.split())
					tokensReview = tokenizer(rmSPace)
					regex = re.compile('[1-9+.,-;@_!#$%^&*()<>?/\\\|}{~:]')
					for indTok in tokensReview:
						if regex.search(indTok.lower_) == None:
							if indTok.lower_ not in gutenToks:
								tokensRev[indTok.lower_] += 1
					cmbndLstTxtTokfreq = addToks(tokensRev, cmbndLstTxtTokfreq)

					expressionHere = defaultdict(lambda:0)
					for invMath in obj["formulaeMathML"]:
						soupMath = BeautifulSoup(invMath[list(invMath.keys())[0]][2], "html.parser")
						decsMain = set()
						chldrns = [desc for desc in soupMath.children]
						firstChld = [desc.get_text() for desc in chldrns[0]]
						combndList = list()
						for ele in firstChld:
							if len(ele)==1:
								combndList.append(ele)
								combndList = "".join(combndList)
								expressionHere[combndList[0]] += 1
						for desc in soupMath.descendants:
							#I know this counts single constants s.a. A, B, Y, X as extra
							#but since anyways we do not use singe ocurances then ignore now
							#Else worse case subtract 1 from single id count by count occurrances of these
							if desc.name in ["mrow","mpadded","mrrot","math","msqrt",
							"mfrac","mover", "mroot"]:
								decsMain.add(desc.get_text())
						for mdesc in decsMain:
							expressionHere[mdesc] += 1
					cmbndLstMthTokfreq = addToks(expressionHere, cmbndLstMthTokfreq)
					jsonDraft["docID"] = obj["docID"]
					jsonDraft["reviews"] = tokensRev
					jsonDraft["formulaeMathML"] = expressionHere
					jsonDraft["msc"] = obj["msc"]
					#writerOPr.write(jsonDraft)

					for idH in randSamplecorp.keys():
						if obj["docID"] in randSamplecorp[idH]:
							rndmSmpsTxtTokfreq[idH] = addToks(tokensRev, rndmSmpsTxtTokfreq[idH])
							rndmSmpsMthTokfreq[idH] = addToks(expressionHere, rndmSmpsMthTokfreq[idH])

	with open("cmbndLstTxtTokfreq.pkl", 'wb') as fa:
		pickle.dump(cmbndLstTxtTokfreq, fa)
	with open("cmbndLstMthTokfreq.pkl", 'wb') as fb:
		pickle.dump(cmbndLstMthTokfreq, fb)
	with open("rndmSmpsTxtTokfreq.pkl", 'wb') as fc:
		pickle.dump(rndmSmpsTxtTokfreq, fc)
	with open("rndmSmpsMthTokfreq.pkl", 'wb') as fd:
		pickle.dump(rndmSmpsMthTokfreq, fd)


def checksampleTOKsfreqtext():
	with open('rndmSmpsMthTokfreq.pkl', 'rb') as fz:
		cmbndLstT = pickle.load(fz)
	print(len(cmbndLstT[0]))	

def addToks(smllDict, bgDict):
	for keys in smllDict.keys():
		bgDict[keys] += smllDict[keys]
	return bgDict


def saveRand(dirToks):
	# dirToks : from function with initial directory
	#START: To get all the dcos from 4623 combination list 
	with open('mscFreDocsRevNew.pkl', 'rb') as fy:
		sampleWithfreq = pickle.load(fy)
	sampleWithfreq = OrderedDict(sorted(sampleWithfreq.items(), key=lambda kv: kv[1][0], reverse=True))

	lstwthnonsngleIDS = list()
	for key in sampleWithfreq.keys():
		if sampleWithfreq[key][0] != 1:
			rvisedLst = list(set(sampleWithfreq[key][1]))
			lstwthnonsngleIDS = lstwthnonsngleIDS + rvisedLst
	#END: To get all the dcos from 4623 combination list

	listOfFreqREF = list()
	allDirs = os.listdir(dirToks)
	for dirhere in allDirs:
		with jsonlines.open(dirToks+"/"+dirhere) as reader:
			for obj in reader:
				if obj["docID"] in lstwthnonsngleIDS:
					if eacTk not in obj["reviews"].keys():
						valFreq = 0
					else:
						valFreq = obj["reviews"][eacTk]
						#print(valFreq)
					listOfFreqREF.append()

	with open("listOfFreqREF.pkl", 'wb') as fd:
		pickle.dump(listOfFreqREF, fd)


def prewilcoxMannUtest():
	with open('randSampleAndTextToks.pkl', 'rb') as fy:
		sampleWithfreq = pickle.load(fy)
	print(list(sampleWithfreq[0])[:10])


def wilcoxMannUtest(dirToks):
	#START: To get all the dcos from 4623 combination list 
	with open('mscFreDocsRevNew.pkl', 'rb') as fy:
		sampleWithfreq = pickle.load(fy)
	sampleWithfreq = OrderedDict(sorted(sampleWithfreq.items(), key=lambda kv: kv[1][0], reverse=True))

	lstwthnonsngleIDS = list()
	for key in sampleWithfreq.keys():
		if sampleWithfreq[key][0] != 1:
			rvisedLst = list(set(sampleWithfreq[key][1]))
			lstwthnonsngleIDS = lstwthnonsngleIDS + rvisedLst
	#END: To get all the dcos from 4623 combination list

	#START: To get dict of randSamp IDS and theri docs
	with open('randSamplecorp.pkl', 'rb') as fn:
		randSampIds = pickle.load(fn)
	#END: To get dict of randSamp IDS and theri docs

	with open("cmbndLstTxtTokfreq.pkl", 'rb') as fz:
		cmbinedToks = pickle.load(fz)
	cmbinedToks = OrderedDict(sorted(cmbinedToks.items(), key=lambda kv: kv[1], reverse=True))
	cmbinedToks = {ke: va for ke, va in cmbinedToks.items() if len(ke) > 3}

	refToksAll = dict()	
	i =0
	for valH in cmbinedToks.keys():
		i += 1
		if i > 1000:
			break
		refToksAll[valH] = cmbinedToks[valH]

	with open("rndmSmpsTxtTokfreq.pkl", 'rb') as fy:
		randSamplesTokfreq = pickle.load(fy)

	sampleWiseUtestPvalues = dict()
	for eachSimp in randSamplesTokfreq.keys():
		print("Working for sample: ",eachSimp)
		sampleIndsort = OrderedDict(sorted(randSamplesTokfreq[eachSimp].items(), key=lambda kv: kv[1], reverse=True))
		sampleIndsort = {ke: va for ke, va in sampleIndsort.items() if len(ke) > 3}

		refToksSampindiv = list()
		for keyComb in refToksAll.keys():
			if keyComb in sampleIndsort:
				refToksSampindiv.append(keyComb)
		
		#remove next cap for publishing
		for eacTk in refToksSampindiv[:10]:
			print("token working within")
			#as opposed to sirting suggesedt by paper, I think it will happen automatically if done using scipy function
			listOfFreqREF = list()
			listOfFreqREP = list()
			allDirs = os.listdir(dirToks)
			pvalues = list()
			for dirhere in allDirs:
				#print(dirhere)
				with jsonlines.open(dirToks+"/"+dirhere) as reader:
					for obj in reader:
						if obj["docID"] in lstwthnonsngleIDS:
							if eacTk not in obj["reviews"].keys():
								valFreq = 0
							else:
								valFreq = obj["reviews"][eacTk]
							listOfFreqREF.append(valFreq)
						if obj["docID"] in randSampIds[eachSimp]:
							if eacTk not in obj["reviews"].keys():
								valFreq = 0
							else:
								valFreq = obj["reviews"][eacTk]
							listOfFreqREP.append(valFreq)
			#print(len(listOfFreqREF), len(listOfFreqREP))
			U1, p = mannwhitneyu(listOfFreqREF[:10], listOfFreqREP[:50], method="exact")
			nx, ny = len(listOfFreqREF[:10]), len(listOfFreqREP[:50])
			U2 = nx*ny - U1
			pvalues.append([U1, U2, p])
			#print("U1 and U2 and p", U1, U2, p)
			#sys.exit(0)
		sampleWiseUtestPvalues[eachSimp] = pvalues
	with open("sampleWiseUtestPvalues.pkl", 'wb') as fd:
		pickle.dump(sampleWiseUtestPvalues, fd)


def spearmanCorrrow():
	"""
	Just run this function to see the spearman and p value (For text)
	For math: replace "cmbndLstTxtTokfreq.pkl" with math one (you know which one)
	"""
	with open("cmbndLstMthTokfreq.pkl", 'rb') as fz:
		cmbinedToks = pickle.load(fz)
	cmbinedToks = OrderedDict(sorted(cmbinedToks.items(), key=lambda kv: kv[1], reverse=True))
	cmbinedToks = {ke: va for ke, va in cmbinedToks.items() if len(ke) > 3}

	refToksAll = dict()	
	i =0
	for valH in cmbinedToks.keys():
		i += 1
		if i > 1000:
			break
		refToksAll[valH] = cmbinedToks[valH]

	with open("rndmSmpsMthTokfreq.pkl", 'rb') as fy:
		randSamplesTokfreq = pickle.load(fy)

	for eachSimp in randSamplesTokfreq.keys():
		sampleIndsort = OrderedDict(sorted(randSamplesTokfreq[eachSimp].items(), key=lambda kv: kv[1], reverse=True))
		sampleIndsort = {ke: va for ke, va in sampleIndsort.items() if len(ke) > 3}

		refToksSampindiv = dict()
		for keyComb in refToksAll.keys():
			if keyComb in sampleIndsort:
				refToksSampindiv[keyComb] = sampleIndsort[keyComb]

		refToksSampindiv = OrderedDict(sorted(refToksSampindiv.items(), key=lambda kv: kv[1], reverse=True))
		differSumm = 0
		j = 0
		for keyComb in refToksAll.keys():
			if keyComb in list(refToksSampindiv.keys()):
				j += 1
				differSumm += (j - list(refToksSampindiv.keys()).index(keyComb)) ** 2

		try:
			spearmanCoe = 1 - ((6*differSumm)/(len(refToksSampindiv)* (len(refToksSampindiv)**2-1)))
			tRef = spearmanCoe * (((len(refToksSampindiv) - 2)/(1 - (spearmanCoe**2))) ** 0.5)
			pVal = 1 - t.cdf(x=tRef, df=len(refToksSampindiv)-2)
			print("Spearman Coe on MSC: ",eachSimp, len(refToksSampindiv), spearmanCoe, pVal)	
		except:
			print("Spearman Coe on MSC: ",eachSimp, len(refToksSampindiv),  spearmanCoe, "lolNothing")

		#sys.exit(0)

def T_c():
	"""
	Do for Wilcoxon first then you can do this IDIOT
	"""
	with open("cmbndLstTxtTokfreq.pkl", 'rb') as fz:
		cmbinedToks = pickle.load(fz)
	cmbinedToks = OrderedDict(sorted(cmbinedToks.items(), key=lambda kv: kv[1], reverse=True))
	cmbinedToks = {ke: va for ke, va in cmbinedToks.items() if len(ke) > 3}
	refTokSampAll = set(cmbinedToks)

	with open("rndmSmpsTxtTokfreq.pkl", 'rb') as fy:
		randSamplesTokfreq = pickle.load(fy)

	for eachSimp in randSamplesTokfreq.keys():
		sampleIndsort = OrderedDict(sorted(randSamplesTokfreq[eachSimp].items(), key=lambda kv: kv[1], reverse=True))
		sampleIndsort = {ke: va for ke, va in sampleIndsort.items() if len(ke) > 3}

		percTokcov = (len(refToksmscInd.intersection(refToksmscAll))/len(refToksmscAll))*100


#saveRand()
#sampleTOKsfreqtext()
spearmanCorrrow()
#checksampleTOKsfreqtext()
#wilcoxMannUtest()
#prewilcoxMannUtest()