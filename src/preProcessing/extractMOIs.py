import os
import re
import ast
import sys
import webbrowser
import requests
import httplib2
import urllib
import jsonlines
from fake_useragent import UserAgent
import latex2mathml.converter
from selenium import webdriver
from urllib.request import urlopen


def loopingThroughAll(dirhere):
	"""
	Input: Directory of all files
	Output: Get formulae in MathML from review and save in json format along with
	other charact. of documents such as ID, MSC, reviews
	"""
	listAllfiles = os.listdir(dirhere)
	jsondrft = {
		"docID": None,
		"reviews": None,
		"formulaeMathML": None,
		"msc": None
	}
	for everyDir in listAllfiles:
		readFile = open(maindir+"/"+everyDir, encoding="utf-8").read()
		splittingon = readFile.split("\n")
		for eachRcrd in splittingon:
			frmlsrcrd = dict()
			eachRcrd = ast.literal_eval(eachRcrd)
			print("doing for ID: ",eachRcrd["docID"])
			jsondrft["docID"] = eachRcrd["docID"]
			jsondrft["reviews"] = eachRcrd["reviews"]
			jsondrft["msc"] = eachRcrd["msc"]
			listOffrmle = getFormulaefromReviews(eachRcrd["reviews"])
			print(listOffrmle)
			sys.exit(0)
			for idq,eachfrm in enumerate(listOffrmle):
				frmlsrcrd[idq] = latexToMathML(eachfrm)
				#print("Formula: ",eachfrm,"math converted ", latexToMathML(eachfrm))
			jsondrft["formulaeMathML"] = frmlsrcrd


def latexToMathML(ltexFormula):
	"""
	latex2mathml to convert LaTex to MathML.
	HIGHLY RECOMMENDED TO USE LaTeXML instead of this
	"""
	mathml_output = latex2mathml.converter.convert(ltexFormula)
	return mathml_output



def getFormulaefromReviews(reviewText):
	"""
	Input: Review text
	Output: Formulae extracted in LaTeX and converted to MathML
	"""
	list_math_eqs = list()
	i = 0
	normalBrac = False
	sqrBrac = False
	while i < len(reviewText):
		#check if first index goes out of bound
		if i+2 > len(reviewText): break
		temp_twochars = reviewText[i:i+2]
		if temp_twochars == str(r"\(") or temp_twochars == str(r"\["):  #matching two characters at a time
			if temp_twochars == str(r"\("):
				normalBrac = True
			if temp_twochars == str(r"\["):
				sqrBrac = True
			for j in range(i+2, len(reviewText)):
				next_temp_twochars = reviewText[j:j+2]  #next two characters
				if normalBrac:
					if next_temp_twochars == r"\)":
						inzwischen_chars = reviewText[i+2:j]  #get equation between two wrapper "\(.....\)"
						list_math_eqs.append(inzwischen_chars)
						#print("Detected math: ",inzwischen_chars)
						i = i+2   #set index to chracter after last "\("
						break
				if sqrBrac:
					if next_temp_twochars == r"\]":
						inzwischen_chars = reviewText[i+2:j]  #get equation between two wrapper "\(.....\)"
						list_math_eqs.append(inzwischen_chars)
						#print("Detected math: ",inzwischen_chars)
						i = i+2   #set index to chracter after last "\("
						break
		else:
			i = i+1   #if no matches found then go to the next characters
	return list_math_eqs


def latex2svg(latexcode):
	"""
	Turn LaTeX string to an SVG formatted string using the online SVGKit
	found at: http://svgkit.sourceforge.net/tests/latex_tests.html
	"""
	txdata = urllib.parse.urlencode({"latex": latexcode})
	url = "http://svgkit.sourceforge.net/cgi-bin/latex2svg.py"
	req = urllib.request(url, txdata)
	return urllib.request.urlopen(req).read()


def mathTokFreq(docList):
	dirALl = os.listdir(docList)
	mainSubExpFreq = defaultdict(lambda:0)
	for diri in dirALl:
		with jsonlines.open(docList+"/"+diri, mode="r") as readerOP:
			print("for directory: ",diri)
			for redrH in readerOP:
				for invMath in redrH["formulaeMathML"]:
					soupMath = BeautifulSoup(invMath[list(invMath.keys())[0]][2], "html.parser")
					#soupMath = BeautifulSoup(strJocpol, "html.parser")
					#print(soupMath)
					decsMain = set()
					descSub = list()
					chldrns = [desc for desc in soupMath.children]
					firstChld = [desc.get_text() for desc in chldrns[0]]
					combndList = list()
					for ele in firstChld:
						if len(ele)==1:
							combndList.append(ele)
					combndList = "".join(combndList)
					mainSubExpFreq[combndList] += 1
					#sys.exit(0)
					for desc in soupMath.descendants:
						if desc.name in ["mrow","mpadded","mrrot","math","msqrt",
						"mfrac","mover", "mroot"]:
							decsMain.add(desc.get_text())
						else:
							descSub.append(desc.get_text())
					# descendents = [desc.get_text() for desc in soupMath.descendants if desc.name in ["mrow",
					# "msubsup", "math"]]
					# descendentsOth = [desc.get_text() for desc in soupMath.descendants if desc.name not in ["mrow",
					# "msubsup", "math"]]
					for mdesc in decsMain:
						mainSubExpFreq[mdesc] += 1
					#print(decsMain)
					#print(mainSubExpFreq)
					#a = input("Go ahead: ")
					#sys.exit(0)
	with open('freqMathToksMSC14.pkl', 'wb') as fa:
		pickle.dump(mainSubExpFreq, fa)


def mathTokFreqcounta():
	with open('freqMathToks.pkl', 'rb') as fa:
		dictFreq = pickle.load(fa)
	dictFreq = {k: v for k, v in sorted(dictFreq.items(), key=lambda item: item[1])}
	listKey = list(dictFreq.keys())
	print(len(listKey))
	#sys.exit(0)
	countIdentif = defaultdict(lambda:0)
	for i in listKey:
		countIdentif[len(i)] += 1
	sortedCount = {k: v for k, v in sorted(countIdentif.items(), key=lambda item: item[1])}
	print("dict of length wise expressions: ", sortedCount)

def mathTokFreqcountaRev():
	with open('freqMathToks.pkl', 'rb') as fa:
		dictFreq = pickle.load(fa)
	dictFreq = {k: v for k, v in sorted(dictFreq.items(), key=lambda item: item[1])}
	listKey = list(dictFreq.keys())
	print(len(listKey))
	#sys.exit(0)
	countIdentif = defaultdict(lambda:0)
	for i in listKey:
		if len(i) == 5:
			print(BeautifulSoup(i, "html.parser"), dictFreq[i])
			a = input(" ")
		#countIdentif[len(i)] += 1
	#sortedCount = {k: v for k, v in sorted(countIdentif.items(), key=lambda item: item[1])}
	#print("dict of length wise expressions: ", sortedCount)

def getSiblingtest(disc):
	for i in range(20):
		if disc.next_sibling:
			if disc.next_sibling.name not in ['mi','mo','mn']:
				disc = disc.next_sibling
				break
			else:
				disc = disc.next_sibling
	#print("sibkingtest: ",disc)
	return disc

def checkIfmn(childrnsNMS):
	"""
	This is a function to check if at least a single
	leaf of a last node contains an identifier or not.
	Return:-
	False: if only mn is present
	True: otherwise  
	"""
	lenOegnl = len(childrnsNMS)
	listmn = list()
	for nm in childrnsNMS:
		if nm in ['mn']:
			listmn.append(nm)
	if lenOegnl == len(listmn):
		return False
	else:
		return True

def checkuniqParent(ele, originalEle, strta):
	if str(ele) == str(originalEle):
		return [False, strta]
	elif ele.parent.next_sibling:
		strta -= 1
		#print(ele.parent.next_sibling)
		return [True, strta]
	else:
		strta -= 1
		return checkuniqParent(ele.parent, originalEle, strta)

def getparentWithSibl(ele, strt):
	if ele.parent.next_sibling:
		strt = strt - 1
		return [ele.parent.next_sibling, strt]
	else:
		strt = strt -1
		return getparentWithSibl(ele.parent, strt)

def counChildrens(element, start, originalEle, mnlist):
	if element.children:
		childrns = [child for child in element.children if child.name != None]
		childrnsnms = [child.name for child in element.children if child.name != None]
		if len(childrns) != 0:
			start += 1
			if checkIfmn(childrnsnms): mnlist.append(start)
		#print(start)
		if len(childrns) == 0:
			if element.next_sibling:
				#print("siblings: ",getSiblingtest(element))
				return counChildrens(getSiblingtest(element), start,originalEle, mnlist)
			elif element.parent:
				start -= 1
				#print("parentblock: ",element.parent)
				if str(element.parent) == str(originalEle):
					return [start, mnlist]
				elif element.parent.next_sibling:
					return counChildrens(getSiblingtest(element.parent), start,originalEle, mnlist)
				elif checkuniqParent(element.parent, originalEle, start)[0]:
					hereELe = getparentWithSibl(element.parent, start)
					return counChildrens(hereELe[0],
					hereELe[1],originalEle, mnlist)
				else:
					return [checkuniqParent(element.parent, originalEle, start)[1],mnlist]
			else:
				return [start,mnlist]
		else:
			return counChildrens(childrns[0], start, originalEle, mnlist)
	# elif element.next_sibling:
	# 	print("sibling: ",getSiblingtest())
	# 	counChildrens(getSiblingtest(), start)
	else:
		return [start,mnlist]

def getNodescount(mathSoup):
	listOftags = defaultdict(lambda:0)
	countTags = 0
	for child in mathSoup.descendants:
		if child.name not in ["mi", "mn", "mo", 
		"ms", "mspace","ms","mtext"] and child.name != None:
			listOftags[child.name] += 1
			countTags += 1
	#print(countTags)
	return countTags

def mathfrequnciesMSCwise(pathMscAll):
	"""
	Input: Path with all documents of zbMATH Open
	Please remember to preprocess the dataset.
	"""
	nlp = English()
	tokenizer = nlp.tokenizer
	dir_list = os.listdir(pathMscAll)
	mscmathTokFreq = defaultdict(lambda:defaultdict(lambda:0))
	expressionCompl = defaultdict(lambda:list())
	mathTokComplex = dict()
	undone = defaultdict(lambda:list())
	with open('pickleszbMATH/ohneEngIDSall.pkl', 'rb') as fc:
		ohneEngIDs = pickle.load(fc)
	for dir1 in dir_list:
		print("working with directory: ",dir1)
		with jsonlines.open(pathMscAll+"/"+dir1) as reader:
			for obj in reader:
				localTokDict = defaultdict(lambda:0)
				if obj["docID"] not in ohneEngIDs:
					ohneMath = re.sub(r'\\\(.+?\\\)', '',obj["reviews"])
					ohneSpeMen = re.sub(r'\[.+?\]', '',ohneMath)
					rmSPace = ' '.join(ohneSpeMen.split())
					tokensReview = tokenizer(rmSPace)
					regex = re.compile('[1-9+.,-;@_!#$%^&*()<>?/\\\|}{~:]')
					for indTok in tokensReview:
						if regex.search(indTok.lower_) == None:
							localTokDict[indTok.lower_] += 1
					Tokkcount = sum(localTokDict.values())
				expressionHere = defaultdict(lambda:0)
				for invMath in obj["formulaeMathML"]:
					soupMath = BeautifulSoup(invMath[list(invMath.keys())[0]][2], "html.parser")
					decsMain = set()
					descSub = list()
					chldrns = [desc for desc in soupMath.children]
					firstChld = [desc.get_text() for desc in chldrns[0]]
					combndList = list()
					for ele in firstChld:
						if len(ele)==1:
							combndList.append(ele)
							combndList = "".join(combndList)
							expressionCompl[combndList[0]] = [max(counChildrens(chldrns[0],0,chldrns[0],list())[1])-1,getNodescount(chldrns[0])]
							expressionHere[combndList[0]] += 1
					getVals = dict()
					for desc in soupMath.descendants:
						if desc.name in ["mrow","mpadded","mrrot","math","msqrt",
						"mfrac","mover", "mroot"]:
							decsMain.add(desc.get_text())
							getVals[desc.get_text()] = desc
						else:
							descSub.append(desc.get_text())
					for mdesc in decsMain:
						try:
							expressionCompl[mdesc] = [max(counChildrens(getVals[mdesc],0,getVals[mdesc],list())[1])-1,getNodescount(getVals[mdesc])]
						except:
							expressionCompl[mdesc] = [0,0]
							undone[obj["docID"]].append(list(invMath.keys())[0])
							#print("Document ID: ",list(invMath.keys())[0])
						expressionHere[mdesc] += 1
				try:
					if Tokkcount > 35:
						for msc in obj["msc"]:
							mscmathTokFreq[msc["code"][:2]] = updateMainDict(mscmathTokFreq[msc["code"][:2]],
								expressionHere)
				except:
					print("Doc ID :", obj["docID"])
	with open("mscmathTokFreq.pkl", 'wb') as fk:
		pickle.dump(mscmathTokFreq, fk)
	with open("mscmathTokFreqMathMl.pkl", 'wb') as fk:
		pickle.dump(expressionCompl, fk)
	for eachmSCa in mscmathTokFreq.keys():
		with open("pickleszbMATH/mscWiseMath/mscTokfreq"+str(eachmSCa)+".pkl", 'wb') as fg:
			dictForMSC = dict()
			dictForMSC[eachmSCa] = mscmathTokFreq[eachmSCa]
			pickle.dump(dictForMSC, fg)


def updateMainDict(mainDict, passedDict):
	"""
	Use this function to update the main dict with passed new dict of tokens
	"""
	for key in passedDict.keys():
		mainDict[key] += passedDict[key] 
	return mainDict

#mathfrequnciesMSCwise()
#mathTokFreqcountaRev()
#mathTokFreq(dirMathfin)

maindir = "DIR with all preprocessed documents from zbMATH Open"
loopingThroughAll(maindir)


