import os
import re
import sys
import jsonlines
import dill as pickle
from collections import defaultdict
from spacy.lang.en import English
from collections import defaultdict
from spacy.tokenizer import Tokenizer

dirMathComp = "A:/Study/FIZ/Project/22GoldStandardRecSys/data/Final_ALL/allWithComplexity"
nlp = English()
tokenizer = nlp.tokenizer


def cooutAllstats(hereDIR):
	"""
	Input: dir with all docs and their complexity
	Output: 
	complexDepFreq = dict with keys as all MSCs and values(again as dict) as their 
	depth-complexity content and frequencies.
	complexLenFreq = dict with keys as all MSCs and values(again as dict) as their 
	length-complexity content and frequencies.
	TokensLenFreq = dict with keys as all MSCs and values(again as dict) as their 
	token-lentgh content and frequencies.
	"""
	complexDepFreqAll = defaultdict(lambda:0)
	complexLenFreqAll = defaultdict(lambda:0)
	TokensLenFreqAll = defaultdict(lambda:0)
	complexDepFreq = defaultdict(lambda:defaultdict(lambda:0))
	complexLenFreq = defaultdict(lambda:defaultdict(lambda:0))
	TokensLenFreq = defaultdict(lambda:defaultdict(lambda:0))
	listDirs = os.listdir(hereDIR)
	docsWithNoMSC = list()
	for dirinv in listDirs:
		print("doing for the dir: ",dirinv)
		with jsonlines.open(hereDIR+"/"+dirinv, mode="r") as readerOP:
			for rdr in readerOP:
				localTokfreq = getTokFreq(rdr["reviews"])
				localComp = getComplexitvals(rdr["formulaeMathML"])
				localCompDepth = localComp[0]
				localCompLen = localComp[1]
				complexDepFreqAll = getAllcombined(complexDepFreqAll, localCompDepth)
				complexLenFreqAll = getAllcombined(complexLenFreqAll, localCompLen)
				TokensLenFreqAll = getAllcombined(TokensLenFreqAll, localTokfreq)
				#print(localTokfreq, localCompDepth, localCompLen)
				if isinstance(rdr["msc"], str):
					docsWithNoMSC.append(rdr["docID"])
				else:
					for eachMsc in rdr["msc"]:
						complexDepFreq[eachMsc["code"][:2]] = conCatenateDict(complexDepFreq[eachMsc["code"][:2]],
							localCompDepth)
						complexLenFreq[eachMsc["code"][:2]] = conCatenateDict(complexLenFreq[eachMsc["code"][:2]],
							localCompLen)
						TokensLenFreq[eachMsc["code"][:2]] = conCatenateDict(TokensLenFreq[eachMsc["code"][:2]],
						localTokfreq)
	with open('complexDepFreqAll.pkl', 'wb') as fa:
		pickle.dump(complexDepFreqAll, fa)
	with open('complexLenFreqAll.pkl', 'wb') as fb:
		pickle.dump(complexLenFreqAll, fb)
	with open('TokensLenFreqAll.pkl', 'wb') as fc:
		pickle.dump(TokensLenFreqAll, fc)


	print("Docs with no MSC: has len: ", len(docsWithNoMSC), "and are: ", docsWithNoMSC)
	saveAllDictasPickle([complexDepFreq, complexLenFreq, TokensLenFreq])


def getAllcombined(originaldict, tempdict):
	for key in tempdict.keys():
		originaldict[key]+= tempdict[key]
	return originaldict	


def saveAllDictasPickle(allDicts):
	"""
	Save all dicts as pickle
	"""
	with open('complexDepFreq.pkl', 'wb') as fa:
		pickle.dump(allDicts[0], fa)
	with open('complexLenFreq.pkl', 'wb') as fb:
		pickle.dump(allDicts[1], fb)
	with open('TokensLenFreq.pkl', 'wb') as fc:
		pickle.dump(allDicts[2], fc)

def conCatenateDict(mainDict, tempDict):
	"""
	Input: mainDict, tempDict 
	Output: dict with all keys-value added to mainDict
	"""
	for key in tempDict.keys():
		mainDict[key]+= tempDict[key]
	return mainDict

def getComplexitvals(formuLaedict):
	"""
	Input: dict with formula ID and vals(complexDepth, complexLen, mathMLfmrla)
	Output: 
	locComplDepthFreq = dict with keys as complexityDepth and values as freq
	locComplLenFreq = dict with keys as complexityLength and values as freq
	"""
	locComplDepthFreq = defaultdict(lambda:0)
	locComplLenFreq = defaultdict(lambda:0)
	for key in formuLaedict:
		for inKey in key.keys():
			locComplDepthFreq[key[inKey][0]] += 1
			locComplLenFreq[key[inKey][1]] += 1
	return [locComplDepthFreq, locComplLenFreq]


def getTokFreq(reviewText):
	"""
	Input: review text
	Output: dictionionr= keys as length of present tokens and values
	as frequency of each token lenght
	"""
	tempaFreq = defaultdict(lambda:0)
	ohneMath = re.sub(r'\\\(.+?\\\)', '', reviewText)
	ohneSpeMen = re.sub(r'\[.+?\]', '',ohneMath)
	rmSPace = ' '.join(ohneSpeMen.split())
	tokensReview = tokenizer(rmSPace)
	regex = re.compile('[1-9+.,-;@_!#$%^&*()<>?/\\\|}{~:]')
	for indTok in tokensReview:
		if regex.search(indTok.lower_) == None:
			tempaFreq[len(indTok.lower_)] += 1
	#print(tempaFreq)
	return tempaFreq


cooutAllstats(dirMathComp)