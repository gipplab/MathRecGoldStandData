import os
import re
import sys
import random
import jsonlines
import dill as pickle
from collections import defaultdict, OrderedDict
from spacy.lang.en import English
from spacy.tokenizer import Tokenizer

notAllowedMSCs = ["14-00", "14-01", "14-02", "14-03", "14-04", "14-06", "14-11"]

mscFreqperdoc = defaultdict(lambda:[0,[]])
nlp = English()
tokenizer = nlp.tokenizer


def msc14preprocMSCcombcount(pathMsc14):
	"""
	Check if MSC 14 docs in the folder pathMsc14	- They do not have docs with
		- language other than English (ohneEngIDS.pkl)
		- MSC ["14-00", "14-01", "14-02", "14-03", "14-04", "14-06", "14-11"]
		- less than 35 tokens (listOfsmallDocs.pkl)
		- No reviews and abstract text (String matching)
	"""
	dir_list = os.listdir(pathMsc14)
	countAll = 0
	dictTokfreqAll = defaultdict(lambda:0)
	with open('pickleszbMATH/gutenBergToks.pkl', 'rb') as fr:
		gutenToks = pickle.load(fr)
	for dir1 in dir_list:
		print("working with directory: ",dir1)
		with jsonlines.open(pathMsc14+"/"+dir1) as reader:
			for obj in reader:
				noallowedMSC = True 
				for indmsc in obj["msc"]:
					if indmsc["code"] in notAllowedMSCs:
						noallowedMSC = False
				if noallowedMSC:
					countAll += 1
					ohneMath = re.sub(r'\\\(.+?\\\)', '',obj["reviews"])
					ohneSpeMen = re.sub(r'\[.+?\]', '',ohneMath)
					rmSPace = ' '.join(ohneSpeMen.split())
					tokensReview = tokenizer(rmSPace)
					regex = re.compile('[1-9+.,-;@_!#$%^&*()<>?/\\\|}{~:]')
					for indTok in tokensReview:
						if regex.search(indTok.lower_) == None:
							if indTok.lower_ not in gutenToks:
								dictTokfreqAll[indTok.lower_] += 1
					# locList = list()
					# for msc in obj["msc"]:
					# 	if msc["code"][:2] == "14":
					# 		locList.append(msc["code"])
					# mscFreqperdoc[tuple(locList)][0] += 1
					# mscFreqperdoc[tuple(locList)][1].append(obj["docID"])
				# else:
				# 	countAll += 1
	# with open("mscFreDocsRevNew.pkl", 'wb') as fg:
	# 	pickle.dump(mscFreqperdoc, fg)
	with open("mscFreAll.pkl", 'wb') as fg:
		pickle.dump(dictTokfreqAll, fg)
	print(countAll)


def msc14preprocMSCcombcountCheck():
	with open('mscFreAll.pkl', 'rb') as fr:
		loaded_dict = pickle.load(fr)
	print(len(list(loaded_dict.keys())))	


def loadTokenFreq():
	#with open('pickleszbMATH/mscFreDocs.pkl', 'rb') as fr:
	countwithOne = 0
	with open('mscFreDocsRevNew.pkl', 'rb') as fr:
		loaded_dict = pickle.load(fr)
	print(len(list(loaded_dict.keys())))
	d_descending = OrderedDict(sorted(loaded_dict.items(), key=lambda kv: kv[1][0], reverse=True))
	for key_each in list(d_descending.keys()):
		# if d_descending[key_each][0] == 1:
		# 	countwithOne += 1
		print(key_each, d_descending[key_each][0])
		sys.exit(0)
	print(countwithOne)


def sampleswithIDS():
	"""
	Arranginf MSC combinations and the documents belonging to eack of the combination.
	Output: dict with
	Key = sample ID
	value = list of documents belonging to that comibation (selected random from within a group)
	"""
	with open('mscFreDocsRevNew.pkl', 'rb') as fr:
		loaded_dict = pickle.load(fr)
	randSamplecorp = defaultdict(lambda:list())
	for sampleID in range(0,51):
		print("fr sample: ",sampleID)
		listofIDS = list()
		for key_each in list(loaded_dict.keys()):
			listofIDS.append(random.choice(loaded_dict[key_each][1]))
		randSamplecorp[sampleID] = listofIDS
	with open("randSampleswithIDs.pkl", 'wb') as fz:
		pickle.dump(randSamplecorp, fz)

def randomMSCpairscheck():
	with open('randSampleswithIDs.pkl', 'rb') as fr:
		loaded_dict = pickle.load(fr)
	print(len(set(list(loaded_dict[1]))))
	print(loaded_dict[0])


def freqOfMSCcombinSamples():
	# load gutenberg toks 
	# Pending: Constructing a dict with Tokens and their frequency from each sample. 
	with open('pickleszbMATH/gutenBergToks.pkl', 'rb') as fr:
		gutenToks = pickle.load(fr)
	with open('randSampleswithIDs.pkl', 'rb') as fo:
		randMSCpairs = pickle.load(fo)
	freqDict = defaultdict(lambda:defaultdict(lambda:0))
	listOfdirs = os.listdir(pathMsc14)
	for everyDor in listOfdirs:
		print(everyDor)
		with jsonlines.open(pathMsc14+"/"+everyDor) as reader:
			for obj in reader:
				dictTokfreq = defaultdict(lambda:0)
				ohneMath = re.sub(r'\\\(.+?\\\)', '',obj["reviews"])
				ohneSpeMen = re.sub(r'\[.+?\]', '',ohneMath)
				rmSPace = ' '.join(ohneSpeMen.split())
				tokensReview = tokenizer(rmSPace)
				regex = re.compile('[1-9+.,-;@_!#$%^&*()<>?/\\\|}{~:]')
				for indTok in tokensReview:
					if regex.search(indTok.lower_) == None:
						if indTok.lower_ not in gutenToks:
							dictTokfreq[indTok.lower_] += 1
				for eachSample in randMSCpairs.keys():
					if obj["docID"] in randMSCpairs[eachSample]:
						for keyTok in dictTokfreq.keys():
							freqDict[eachSample][keyTok] += 1
	with open("randSampleswithFreqs.pkl", 'wb') as fz:
		pickle.dump(freqDict, fz)

def freqOfMSCcombinSamplesCheck():
	with open('randSampleswithFreqs.pkl', 'rb') as fr:
		loaded_dict = pickle.load(fr)
	d_descending = OrderedDict(sorted(loaded_dict.items(), key=lambda kv: kv[1][0], reverse=True))
	print(loaded_dict[0])