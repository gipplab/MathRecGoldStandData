import os
import re
import sys
import random
import jsonlines
import dill as pickle #required to pickle lambdas
from collections import defaultdict
from spacy.lang.en import English
from spacy.tokenizer import Tokenizer

nlp = English()
mydir = "A:/dataAlldoc"
tokenizer = nlp.tokenizer
listReviews = os.listdir(mydir)

def getGutenBergToks(dirGut):
	"""
	Input: File with commonly occurring English language words
	Output: List (as a pickle) with unique token.
	"""
	lisofDirs = os.listdir(dirGut)
	dictOfuniqueToks = set()
	for evFile in lisofDirs:
		file = open(dirGut+"/"+evFile, "r", encoding="utf-8").read()
		rmSPace = ' '.join(file.split())
		tokensReview = tokenizer(rmSPace)
		regex = re.compile('[1-9+.,-;@_!#$%^&*()<>?/\\\|}{~:]')
		for indTok in tokensReview:
			if regex.search(indTok.lower_) == None:
				dictOfuniqueToks.add(indTok.lower_)

	with open('gutenBergToks.pkl', 'wb') as f:
		pickle.dump(list(dictOfuniqueToks), f)


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

def subCorpusMSC(naDocs):
	"""
	Select subset of corpus from MSC occurances.
	Return list of IDS to be included in GoldStandard 
	"""
	subCorp = list()
	naDocs = list(set(naDocs))
	with open('pickleszbMATH/mscFreDocs.pkl', 'rb') as fri:
		mscDocsFreq = pickle.load(fri)
	revisedsubCorp = defaultdict()
	for eachMSC in mscDocsFreq.keys():
		listTodel = set()
		for id_i in mscDocsFreq[eachMSC][1]:
			if id_i in naDocs:
				listTodel.add(id_i)
		listTosav = list()
		listTosav.append(mscDocsFreq[eachMSC][0])
		listTosav.append(list(set(mscDocsFreq[eachMSC][1]) - listTodel))
		revisedsubCorp[eachMSC] = listTosav
	#print("length of revised MSC corp without nonenglish and short docs: ",len(revisedsubCorp))

	for eachmSC in revisedsubCorp.keys():
		if len(revisedsubCorp[eachmSC][1]) > 0:
			subCorp.append(random.choice(revisedsubCorp[eachmSC][1]))
	#print(len(subCorp))
	return subCorp

def saveTokenFreq():
	dictTokfreq = defaultdict(lambda:0)
	shortDocs = loadShortDocsList() + loadListIDSohneEng()
	subCorpusDoocs = subCorpusMSC(shortDocs)
	cont = 0
	totalCount = 0
	for everyFile in listReviews:
		with jsonlines.open(mydir+"/"+everyFile) as reader:
			#print("Calculating for file: ",everyFile)
			for obj in reader:
				totalCount += 1
				if obj["docID"] in subCorpusDoocs:
					cont +=1
					ohneMath = re.sub(r'\\\(.+?\\\)', '',obj["reviews"])
					ohneSpeMen = re.sub(r'\[.+?\]', '',ohneMath)
					rmSPace = ' '.join(ohneSpeMen.split())
					tokensReview = tokenizer(rmSPace)
					regex = re.compile('[1-9+.,-;@_!#$%^&*()<>?/\\\|}{~:]')
					for indTok in tokensReview:
						if regex.search(indTok.lower_) == None:
							dictTokfreq[indTok.lower_] += 1
	with open('pickleszbMATH/tokFreq.pkl', 'wb') as f:
	    pickle.dump(dictTokfreq, f)
	#print("Documents should be 26457: ",cont)
	#print("Total documents currently considering are: ",totalCount)
	return subCorpusDoocs

def loadTokenFreq():
	with open('pickleszbMATH/tokFreq.pkl', 'rb') as fr:
	    loaded_dict = pickle.load(fr)
	    #print(len(loaded_dict))
	return loaded_dict

def loadGutenToks():
	with open('pickleszbMATH/gutenBergToks.pkl', 'rb') as fr:
	    loaded_dict = pickle.load(fr)
	    #print(len(loaded_dict))
	return loaded_dict

def loadShortDocsList():
	"""
	Loading documents IDs with tokens less than 35
	"""
	with open('pickleszbMATH/listOfsmallDocs.pkl', 'rb') as fri:
		loaded_dict = pickle.load(fri)
	return loaded_dict

def loadListIDSohneEng():
	"""
	List of IDs with content from other languages.
	"""
	with open('pickleszbMATH/ohneEngIDS.pkl', 'rb') as fri:
		loaded_dict = pickle.load(fri)
	return loaded_dict

def represenToks():
	represToksduct = dict()
	msc14Toks = loadTokenFreq()
	gutenToks = loadGutenToks()
	for everyMSCtok in msc14Toks.keys():
		if everyMSCtok not in gutenToks:
			represToksduct[everyMSCtok] = msc14Toks[everyMSCtok]
	with open('pickleszbMATH/represTokfrew.pkl', 'wb') as f:
	    pickle.dump(represToksduct, f)


def loadRepresenToks():
	with open('pickleszbMATH/represTokfrew.pkl', 'rb') as fria:
		loaded_dict = pickle.load(fria)
	return loaded_dict
