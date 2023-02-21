import os
import sys
import csv
import math
import numpy as np
import jsonlines


def metric_nDCG(resultsFile):
	"""
	# Test cases from wikipedia DCG article
	trueRel = [3,3,3,2,2,2]
	obtainedRel = [3,2,3,0,1,2]
	"""
	totIdrec = 0
	finalnDCG = 0
	countofSeeds = 0
	with jsonlines.open(resultsFile) as reader:
		for obj in reader:
			dCGtrue = 0
			dCGbasel = 0
			toIdeal = len(obj["idealRcmnds"])
			totIdrec += toIdeal

			# print("nDCG: ", totIdrec)

			trueRel = list()
			for te, ele in enumerate(obj["idealRcmnds"]):
				trueRel.append(toIdeal - te)
			obtainedRel = list()
			for idealRec in obj["idealRcmnds"]:
				for key in obj["baselineRcmnds"].keys():
					if int(idealRec) == obj["baselineRcmnds"][key][0]:
						obtainedRel.append(toIdeal - int(key))
			revisedobtRel = list()
			for eachObt in obtainedRel:
				if eachObt < 0:
					revisedobtRel.append(0)
				else:
					revisedobtRel.append(eachObt)
			while len(revisedobtRel) < len(trueRel):
				revisedobtRel.append(0)
			for idh, rel in enumerate(trueRel):
				dCGtrue += (rel/math.log(idh+2, 2))
			for idhh, relh in enumerate(revisedobtRel):
				dCGbasel += (relh/math.log(idhh+2, 2))
			if dCGtrue == 0:
				print("Check size of your ideal recommendatiions")
			else:
				countofSeeds += 1
				finalnDCG += dCGbasel/dCGtrue
	print(finalnDCG/countofSeeds)


def metric_R_at_n(n, resultsFile):
	totalIdealrecomm = 0
	countofSeeds = 0
	with jsonlines.open(resultsFile) as reader:
		for obj in reader:
			toIdeal = len(obj["idealRcmnds"])
			if toIdeal > n:
				topn = obj["idealRcmnds"][:n]
			else:
				topn = obj["idealRcmnds"]
			if toIdeal < 1:
				print("No ideal recommendtions found: ",obj["seed"])
			else:
				countofSeeds += 1
				idealRecIn_n = 0
				for eachRank in obj["baselineRcmnds"].keys():
					if eachRank == 0:
						continue
					else:
						if str(obj["baselineRcmnds"][eachRank][0]) in topn:
							idealRecIn_n += 1
				totalIdealrecomm += (idealRecIn_n/toIdeal)
			# print(toIdeal, idealRecIn_n)
	return totalIdealrecomm/countofSeeds


def metric_MRR(resultsFile):
	recipr_rank = 0
	countofSeeds = 0
	with jsonlines.open(resultsFile) as reader:
		for obj in reader:
			countofSeeds += 1
			for eachIdeal in obj["idealRcmnds"]:
				bslineIds = [str(every[0]) for every in obj["baselineRcmnds"].values()]
				if eachIdeal in bslineIds:
					for eachRank in obj["baselineRcmnds"].keys():
						if eachIdeal in obj["baselineRcmnds"][eachRank]:
							recipr_rank += 1/int(eachRank)
	return recipr_rank/countofSeeds

def metric_P_at_n(n, resultsFile):
	totalIdealrecomm = 0
	countofSeeds = 0
	hereRes = list()
	with jsonlines.open(resultsFile) as reader:
		for obj in reader:
			toIdeal = len(obj["idealRcmnds"])
			if toIdeal > n:
				topn = obj["idealRcmnds"][:n]
			else:
				topn = obj["idealRcmnds"]
			if toIdeal < 1:
				print("No idea recommendtions found: ",obj["seed"])
			else:
				countofSeeds += 1
				idealRecIn_n = 0
				for eachRank in obj["baselineRcmnds"].keys():
					if eachRank == 0:
						continue
					else:
						if str(obj["baselineRcmnds"][eachRank][0]) in topn:
							idealRecIn_n += 1
				hereRes.append([idealRecIn_n,n])
				totalIdealrecomm += (idealRecIn_n/len(topn))
		# print(hereRes)
		# print(toIdeal, idealRecIn_n)
	return totalIdealrecomm/countofSeeds


resultsFilefilt = "Generated recommendation in JSONL file"
# resultsFile = "A:/Study/FIZ/Project/elasticSearch_ex/src/data/old/resultsJsonl.jsonl"
print("metric_P_at_5: ", metric_P_at_n(5, resultsFilefilt))
# print("metric_P_at_3: ", metric_R_at_n(3, resultsFilefilt))
# print("MRR: ", metric_MRR(resultsFile))
# metric_nDCG(resultsFile)
