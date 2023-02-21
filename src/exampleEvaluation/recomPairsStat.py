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


def getAll420Rec(fileLoc):
	"""
	Input: Repository file with seeds and ranked recommendations
	Output: All documents with zbMATH Open IDs
	"""
	listall = list()
	with open(fileLoc, encoding='utf-8') as csvfilereader:
		csvFile = csv.reader(csvfilereader)
		for lines in csvFile:
			IdsandRec = list(filter(None, lines))
			listall = listall + IdsandRec
	return listall

def docLen(pathMscAll):
	"""
	Inpuit: All documents
	Output: Lnegth of document in terms of tokesn in reviews
	"""
	dir_list = os.listdir(pathMscAll)
	count = 0
	listOfsizes = list()
	for dir1 in dir_list:
		print("working with directory: ",dir1)
		with jsonlines.open(pathMscAll+"/"+dir1) as reader:
			for obj in reader:
				if obj["docID"] in list(set(getAll420Rec())):
					listOfsizes.append(len(obj["reviews"].split(" ")))
					count += 1

	print(sum(listOfsizes)/count)


def avgMathPerDoc(pathMscAll):
	"""
	Average math per documents given all IDs
	"""
	dir_list = os.listdir(pathMscAll)
	count = 0
	listOfsizes = list()
	for dir1 in dir_list:
		print("working with directory: ",dir1)
		with jsonlines.open(pathMscAll+"/"+dir1) as reader:
			for obj in reader:
				if obj["docID"] in list(set(getAll420Rec())):
					listOfsizes.append(len(obj["formulaeMathML"]))
					count += 1
	print(sum(listOfsizes)/count)



def seedRecomMathExpre():
	"""
	Math expressions per recommendation pair
	"""
	dictCountmatheq = defaultdict(lambda:0)
	pathMscAll = "C:/Users/asa/Desktop/Projects/22Math_recSys/data/Final_ALL/TOKsall"
	dir_list = os.listdir(pathMscAll)
	count = 0
	listOfsizes = list()
	for dir1 in dir_list:
		print("working with directory: ",dir1)
		with jsonlines.open(pathMscAll+"/"+dir1) as reader:
			for obj in reader:
				if obj["docID"] in list(set(getAll420Rec())):
					dictCountmatheq[obj["docID"]] = len(obj["formulaeMathML"])

	with open("dictCountmatheq.pkl", 'wb') as fk:
		pickle.dump(dictCountmatheq, fk)	



# docLen()
# seedRecomMathExpre()
# avgMathPerDoc()