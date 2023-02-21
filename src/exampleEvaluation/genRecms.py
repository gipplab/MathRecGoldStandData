import os
import sys
import csv
import requests
import mdtex2html
import jsonlines
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch

es = Elasticsearch()
jsonDraft = {
	"seed": None,
	"idealRcmnds": None,
	"baselineRcmnds": None
}


def checkLang(dirCSV):
	"""
	To check the number of documents from the ideal recommendations with
	language other than English
	"""
	setLang = set()
	with jsonlines.open("recsText.jsonl", mode="w") as writerOPr:
		with open(dirCSV, mode ='r') as csvfile:
			csvFile = csv.reader(csvfile)
			for lines in csvFile:
				IdsandRec = list(filter(None, lines))
				for eachdoc in IdsandRec:
					try:
						setLang.add(getDocContent(eachdoc))
						if getDocContent(eachdoc) == "German":
							print("in German: ",eachdoc)
					except:
						print(eachdoc)
	print(setLang)

def removeMath(reviewText):	
	"""
	Remove math using mdtex2html
	Convert text --> HTML --> extract text
	"""
	reviewRevised = mdtex2html.convert(reviewText)
	sup = BeautifulSoup("<html><body>"+reviewRevised+"</body></html>", "html.parser")
	return sup.find("p").getText()

def getDocContent(docID):
	recomms = es.search(index="zbmath_live_documents_2022_02_14_19_35_34",
		body={"_source": ["reviews.text","reviews.language"],
		"query":
		{
		"match_phrase":{
		"id": docID
		}},
		})
	# Adjust the return according to your ES indices
	# Following returns language (to check language of the doc)
	# return recomms["hits"]["hits"][0]["_source"]["reviews"][0]["language"]
	# Following return anguage
	return recomms["hits"]["hits"][0]["_source"]["reviews"][0]["text"]

def getTopnRecommn(docContent, n):
	recomms = es.search(index="zbmath_my",
		body={"_source": ["id","score"],
		"size": n,
		"query":
		{
		"match":{
		"reviewstextonly": docContent
		}},
		})
	similarResults = recomms["hits"]["hits"]
	rankedResults = dict()
	rank = 0
	#Rank 0 would be document itself hence not considered
	for eachRes in similarResults:
		# Savinf returned ID and Score in a dict with keys as ranks
		rankedResults[rank] = [eachRes["_id"], eachRes["_score"]]
		rank += 1
	return rankedResults

def loopingTHRseeds(dirCSV):
	#for saving results to jsonlines file
	with jsonlines.open("recsText30.jsonl", mode="w") as writerOPr:
		# for looping thourgh all seeds from the csv file
		with open(dirCSV, mode ='r') as csvfile:
			# reading the CSV file
			csvFile = csv.reader(csvfile)
			# displaying the contents of the CSV file
			for lines in csvFile:
				IdsandRec = list(filter(None, lines))
				seedID = IdsandRec[0]
				print("Calcultaing for seed: ",seedID)
				try:
					recmndtnsIDs = IdsandRec[1:]
					seedContent = getDocContent(seedID)
					seedonlyText = removeMath(seedContent)
					rankedResults = getTopnRecommn(seedonlyText, 100)
					jsonDraft["seed"] = seedID
					jsonDraft["idealRcmnds"] = recmndtnsIDs
					jsonDraft["baselineRcmnds"] = rankedResults
					writerOPr.write(jsonDraft)
				except:
					print("problem with ES?")


dirSeedsandidealRec = "/seeds_idealrecomms.csv"
loopingTHRseeds(dirSeedsandidealRec)
# checkLang(dirSeedsandidealRec)