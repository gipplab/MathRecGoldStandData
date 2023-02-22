import os
import re
import sys
import csv
import random
import json
import jsonlines
import dill as pickle
from spacy.lang.en import English
from bs4 import BeautifulSoup
from collections import defaultdict, OrderedDict
from spacy.tokenizer import Tokenizer


#Es instance
es = Elasticsearch()

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}
#boilerplate to save retrived doc IDs
jsonDraft = {
	"seed": None,
	"idealRcmnds": None,
	"baselineRcmnds": None
}

def getmainIDSandSave(dirRec):
	"""
	Dinputdir: All documents with working dataset
	Output: FInal represent sample
	"""
	countRecommends = 0
	textFile = open("textBIB.txt", "w")
	with open(dirRec+"idealRecommendations.csv", mode ='r') as csvfile:
		csvFile = csv.reader(csvfile)
		for lines in csvFile:
			IdsandRec = list(filter(None, lines))
			for eachDOc in IdsandRec: 
				countRecommends += 1
				try:
					zbl = getZBLid(eachDOc)
					if int(eachDOc) == zbl["id"]:
						bp1 = "https://zbmath.org/bibtex/"
						bp2 = ".bib"
						print(bp1+zbl["identifier"]+bp2)
						req = requests.get(bp1+zbl["identifier"]+bp2, headers)
						soup = BeautifulSoup(req.content, 'html.parser')
						textFile.write(soup.prettify())
				except:
					print(eachDOc)
	print(countRecommends)


def getTopnRecommn(docContent):
	recomms = es.search(index="temp_zbmath_my",
		body={"_source": ["id","score"],
		"size": n,
		"query":
		{
		"match":{
		"reviews.text": docContent
		}},
		})
	similarResults = recomms["hits"]["hits"]
	rankedResults = dict()
	rank = 0
	#Rank 0 would be document itself hence not considered
	for eachRes in similarResults:
		# Savinf returned ID and Score in a dict with keys as ranks
		rankedResults[rank] = [eachRes["_source"]["id"], eachRes["_score"]]
		rank += 1
	return rankedResults


def getZBLid(internalID):
	recomms = es.search(index="temp_zbmath_my",
		body={"_source": ["identifier","id"],
		"query":
		{
		"match_phrase":{
		"id": internalID
		}},
		})
	similarResults = recomms["hits"]["hits"][0]["_source"]
	return similarResults


def verifyZBLid():
	dirRec = "C:/Users/asa/Desktop/Projects/22Math_recSys/Code/Indexing_formuale_on_ES/code/baseline/idealRecommnds/"
	textOpen = open("docsWithpdfs.txt").read()
	downloadedDocs = list(textOpen.split("\n"))
	headerH = ["document ID"]
	# print(type(list(textOpen.split("\n"))[0]))
	with open(dirRec+"idealRecommendationsInaLine.csv", mode ='w') as csvfilewriter:
		writeCSV = csv.writer(csvfilewriter)
		listWitAllIds = set()
		with open(dirRec+"idealRecommendations.csv", mode ='r') as csvfile:
			csvFile = csv.reader(csvfile)
			for lines in csvFile:
				IdsandRec = list(filter(None, lines))
				for eachDOc in IdsandRec:
					try:
						zbl = getZBLid(eachDOc)["identifier"]
						if zbl in downloadedDocs:
							print(type(zbl))
							sys.exit(0)
						else:
							listWitAllIds.add(eachDOc)
					except:
						continue
		# print(list(listWitAllIds)[:10])
		writeCSV.writerow(headerH)
		for eachID in list(listWitAllIds):
			writeCSV.writerow([eachID])	