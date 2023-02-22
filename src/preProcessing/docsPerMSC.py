import os
import re
import sys
import random
import jsonlines
import dill as pickle #required to pickle lambdas
from collections import defaultdict
from spacy.lang.en import English
from spacy.tokenizer import Tokenizer


def loadDocsTest():
# Loading alreayd calculated frequncy values for disciplines
	with open('pickleszbMATH/complexity/final/DepFreq.pkl', 'rb') as fa:
		complexDepFreq = pickle.load(fa)
	with open('pickleszbMATH/complexity/final/LenFreq.pkl', 'rb') as fb:
		complexLenFreq = pickle.load(fb)
	with open('pickleszbMATH/complexity/final/LenFreq.pkl', 'rb') as fc:
		TokensLenFreq = pickle.load(fc)
	return complexDepFreq, complexLenFreq, TokensLenFreq

def percFreqMSCs(mscVals):
	#print(sorted(list(mscVals[])))
	mainDict = dict()
	for indMSC in mscVals.keys():
		valsmsc = list(mscVals[indMSC].values())
		newdictms = dict()
		total = 0
		for val in valsmsc:
			total += val
		for ke in mscVals[indMSC].keys():
			newdictms[ke] = (mscVals[indMSC][ke]/total)*100
		mainDict[indMSC] = newdictms
		#print(mainDict)
	with open('TokensLenFreqperc.pkl', 'wb') as fa:
		pickle.dump(mainDict, fa)

def percentFreq(dictVals):
	cmpl = dict(sorted(dictVals.items()))
	cmplKeys = list(dictVals.keys())
	cmplVals = list(dictVals.values())
	total = 0
	for cm in cmplVals:
		total += cm
	finalFreq = dict()
	for key in dictVals.keys():
		finalFreq[key] = (dictVals[key]/total)*100
	#percFreq = [(val/total)*100 for val in cmplVals]
	print(finalFreq)
	with open('TokensLenFreqAllperc.pkl', 'wb') as fa:
		pickle.dump(finalFreq, fa)


#percFreqMSCs(TokensLenFreq)