import os
import sys
import csv
import jsonlines

csvALLdocs = "Enter location of all zbMATH Open CSV file obtained from URL: https://zenodo.org/record/6448360#.Y_UmrHbP02w"

def allzbMATHfilesasTXT(input_dir, output_dir):
	"""
	Input: CSV file woith all zbMATH Open entries
	Output: All documents as separate files.
	"""
	with open(input_dir, 'r', encoding='utf-8') as csv_file:
	        reader = csv.reader(csv_file)
	        next(reader)  # skip the header row
	        for i, row in enumerate(reader):
	            output_file = os.path.join(output_dir, f'entry_{i}.txt')
	            with open(output_file, 'w', encoding='utf-8') as text_file:
	                text_file.write('\n'.join(row))

def testPrev():
	#Useless
	with open('pickleszbMATH/ohneEngIDS.pkl', 'rb') as fy:
		sampleWithfreq = pickle.load(fy)
	print(len(sampleWithfreq))

def frequnciesMSCwise(pathMscAll):
	nlp = English()
	tokenizer = nlp.tokenizer
	dir_list = os.listdir(pathMscAll)
	mscTokFreq = defaultdict(lambda:defaultdict(lambda:0))
	with open('pickleszbMATH/gutenBergToks.pkl', 'rb') as fa:
		gutenToks = pickle.load(fa)
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
							#check gutenToks later once you know if to consider the doc or not
							localTokDict[indTok.lower_] += 1
					Tokkcount = sum(localTokDict.values())
					uplocalTokDict = dict()
					for eackTok in localTokDict.keys():
						if eackTok not in gutenToks:
							uplocalTokDict[eackTok] =localTokDict[eackTok] 
					try:
						if Tokkcount > 35:
							for msc in obj["msc"]:
								mscTokFreq[msc["code"][:2]] = updateMainDict(mscTokFreq[msc["code"][:2]],
									uplocalTokDict)
					except:
						print("Doc ID :", obj["docID"])
	with open("mscTokfreq.pkl", 'wb') as fk:
		pickle.dump(mscTokFreq, fk)	

	for eachmSCa in mscTokFreq.keys():
		with open("pickleszbMATH/mscWise/mscTokfreq"+str(eachmSCa)+".pkl", 'wb') as fg:
			dictForMSC = dict()
			dictForMSC[eachmSCa] = mscTokFreq[eachmSCa]
			pickle.dump(dictForMSC, fg)

def updateMainDict(mainDict, passedDict):
	"""
	Use this function to update the main dict with passed new dict of tokens
	"""
	for key in passedDict.keys():
		mainDict[key] += passedDict[key] 
	return mainDict

def testRecrdFreq():
	#MSC toke frequencies
	# with open('mscTokfreq.pkl', 'rb') as fy:
	# 	sampleWithfreq = pickle.load(fy)
	# print(len(sampleWithfreq["01"]))
	#MathToksFrequencies<
	# The two pkls freqMathToks and freqMathToksMSC14 have math tokes as overall
	#but not tokens according to each MSC category and we would need that
	with open('freqMathToks.pkl', 'rb') as fy:
		sampleWithfreq = pickle.load(fy)
	print(list(sampleWithfreq.values())[:10])	


def testMSCgroupsMSC14():
	with open('pickleszbMATH/randomMSC14/mscFreDocsRevNew.pkl', 'rb') as fy:
		sampleWithfreq = pickle.load(fy)
	sampleWithfreq = OrderedDict(sorted(sampleWithfreq.items(), key=lambda kv: kv[1][0], reverse=True))
	#print(list(sampleWithfreq.keys())[:10])
	mxLen = [len(a) for a in list(sampleWithfreq.keys())]
	print(max(mxLen))
	lstCnt = [a[0] for a in list(sampleWithfreq.values()) if a[0] == 1]
	#print(len(lstCnt))



inputDIr = "C:inputALL.csv"
outputDIr = "C:"

allzbMATHfilesasTXT(inputDIr, outputDIr)

# testMSCgroupsMSC14()
#testRecrdFreq()
#frequnciesMSCwise()
#testPrev()