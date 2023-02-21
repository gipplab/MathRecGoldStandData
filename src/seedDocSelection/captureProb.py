import os
import re
import sys
import math
import dill as pickle #required to pickle lambdas
import jsonlines
from collections import defaultdict
from tokenFrequencies import saveTokenFreq, represenToks
from spacy.lang.en import English
from spacy.tokenizer import Tokenizer

def tokBySize():
	"""
	Output: Dictionary with keys as Token lengths and values with a
	dictionary with keys as actual tokens and its freuency.
	"""
	tokWTsize = defaultdict(lambda:dict())
	represToks = loadRepresenToks()
	for each_tok in represToks.keys():
		tokWTsize[len(each_tok)][each_tok] = represToks[each_tok]
	#print(tokWTsize[7])
	tokWTsizePro = defaultdict(lambda:dict())
	for eachSize in tokWTsize.keys():
		if eachSize not in [0]:
			tokWTsizePro[eachSize] = tokWTsize[eachSize]
	return tokWTsizePro


def loadRepresenToks():
	"""
	Required: Representative token frequncies for TOIs and MOIs
	"""

	with open('pickleszbMATH/represTokfrew.pkl', 'rb') as fria:
	#with open('pickleszbMATH/represTokfrew.pkl', 'rb') as fria:
		loaded_dict = pickle.load(fria)
	return loaded_dict

def countOftotalTokens():
	preprocessedToks = tokBySize()
	countOftokens = 0
	for keySize in preprocessedToks.keys():
		for inKeys in preprocessedToks[keySize].keys():
			countOftokens += 1
	#print(countOftokens)


def overallFreq(keysize, mainDict, ovrlTokcnt):
	"""
	Gives outbput b_j
	"""
	allWordodSize = mainDict[keysize]
	ttlOccKey = 0
	for everyWord in allWordodSize.keys():
		ttlOccKey += allWordodSize[everyWord]
	return ttlOccKey/ovrlTokcnt
	
def granularProb(dictWithTokVal, sml_n, cap_N, ovrlTokcn):
	"""
	Given output P_j
	"""
	ttlTokSize_i = 0
	for uniqwrds in dictWithTokVal.keys():
		ttlTokSize_i += dictWithTokVal[uniqwrds]
	probSumm = 0
	#a_ij = 0
	for uniqwrds in dictWithTokVal.keys():
		#check this if right, especcially aij shoul not be +=
		#a_ij += dictWithTokVal[uniqwrds] / ttlTokSize_i
		a_ij = dictWithTokVal[uniqwrds] / ttlTokSize_i
		f_i = dictWithTokVal[uniqwrds] / ovrlTokcn
		lambda_i = f_i/(cap_N/sml_n)
		prob_m = 1 - math.exp(- lambda_i)
		probSumm += a_ij * prob_m
	#print(a_ij)
	return probSumm


def captureProbab(sampleSize, smllTolrgTok):
	n = sampleSize
	N = 22892 #Our working dataset size
	ovrlTokcnt = 0
	for keySize in smllTolrgTok.keys():
		for inKeys in smllTolrgTok[keySize].keys():
			ovrlTokcnt += smllTolrgTok[keySize][inKeys]
	numrTr = 0
	denTr = 0
	for keySize in smllTolrgTok.keys():
		if keySize > 4:
			b_j = overallFreq(keySize, smllTolrgTok, ovrlTokcnt)
			denTr += b_j
			for inKeys in smllTolrgTok[keySize].keys():
				P_J = granularProb(smllTolrgTok[keySize], 
					n, N, ovrlTokcnt)
				numrTr += b_j * P_J
	aggcapProb = numrTr / denTr
	#print(numrTr, denTr)
	return aggcapProb

#print(len(tokBySize()))
#print("Agg capture Prob with 8000 docs : ",captureProbab(8000,tokBySize()))


def loopingForMultipleMSCs():
	listExps = defaultdict(lambda:0)
	for i in range(20):
		corpusDocs = saveTokenFreq()
		represenToks()
		cpProb = captureProbab(50,tokBySize())
		print("Agg capture Prob: ",cpProb)
		listExps[i] = [corpusDocs, cpProb]

	with open('pickleszbMATH/expsMultiple.pkl', 'wb') as f:
		pickle.dump(listExps, f)

#loopingForMultipleMSCs()

# with open('pickleszbMATH/expsMultiple.pkl', 'rb') as fa:
# 	dictPur = pickle.load(fa)
# 	for keya in dictPur.keys():
# 		print(keya, " ", len(dictPur[keya][0]), dictPur[keya][1])


with open('pickleszbMATH/listOfsmallDocs.pkl', 'rb') as fria:
	#with open('pickleszbMATH/represTokfrew.pkl', 'rb') as fria:
	loaded_dict = pickle.load(fria)
	print(loaded_dict[:20])