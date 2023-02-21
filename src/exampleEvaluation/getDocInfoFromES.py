import os
import re
import sys
import random
import jsonlines
import dill as pickle
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch

es = Elasticsearch()

def rndomDocsOlaf():
	"""
	Please change if you use differrent index name.
	This script is for getting documents specific to a reviewer.
	"""
	ids = set()
	allIds = list()
	docsOlaf = es.search(index="temp_zbmath_my",
		body={"_source": ["id"],
		"size": 10000,
	 	"query": {
	   		"bool": {
	     	"must": [
	        	{ "wildcard": { "msc.code": "14*" } }
	      	],
	     	"must_not": [{ 
	       		"wildcard": {
	     		"reviews.reviewer.name": "*Teschke"
	    		}
	    	}]
	 	}
	 	}},
		sort = ["id"])	
	
	allIds = allIds + docsOlaf["hits"]["hits"]
	idTostartwith = docsOlaf["hits"]["hits"][9999]["_id"]

	for i in range(9):
		docsOlafrev = es.search(index="temp_zbmath_my",
			body={"_source": ["id"],
			"size": 10000,
		 	"query": {
		   		"bool": {
		     	"must": [
		        	{ "wildcard": { "msc.code": "14*" } }
		      	],
		     	"must_not": [{ 
		       		"wildcard": {
		     		"reviews.reviewer.name": "*Teschke"
		    		}
		    	}]
		 	}
		 	},
		 	"search_after" : [idTostartwith]
		 	},
			sort = ["id"])
		allIds = allIds + docsOlafrev["hits"]["hits"]
		idTostartwith = docsOlafrev["hits"]["hits"][len(docsOlafrev["hits"]["hits"])-1]["_id"]

	for each in docsOlaf["hits"]["hits"]:
		randEle = random.choice(docsOlaf["hits"]["hits"])
		ids.add(randEle["_id"])
		if len(ids) > 20:
			break

	print(ids)


# rndomDocsOlaf()

def docsWithoutEng():
	ohneEngMSC14 = es.search(index="temp_zbmath_my",
		body={"_source": ["id"],
		"size": 15000,
	 	"query": {
	   		"bool": {
	     	"must": [
	        	{ "wildcard": { "msc.code": "14*" } }
	      	],
	     	"must_not": [{ 
	       		"wildcard": {
	     		"reviews.language": "English"
	    		}
	    	}]
	 	}
	 	}
	 	},
		sort = ["id"])

	print(len(ohneEngMSC14["hits"]["hits"]))

	listofIDS = list()

	for everyEle in ohneEngMSC14["hits"]["hits"]:
		listofIDS.append(everyEle["_id"])

	print(listofIDS[1200])

	with open('ohneEngIDS.pkl', 'wb') as fr:
		pickle.dump(listofIDS, fr)


def docsWithoutEngAll():

	setAllnonenglishIDs = list()

	ohneEngMSC14 = es.search(index="temp_zbmath_my",
		body={"_source": ["id"],
		"size": 100000,
	 	"query": {
	   		"bool": {
	     	"must_not": [{ 
	       		"wildcard": {
	     		"reviews.language": "English"
	    		}
	    	}]
	 	}
	 	}},
		sort = ["id"])

	print(len(ohneEngMSC14["hits"]["hits"]))

	for everyInner in ohneEngMSC14["hits"]["hits"]:
		setAllnonenglishIDs.append(everyInner["_id"])

	idTostartwith = ohneEngMSC14["hits"]["hits"][(len(ohneEngMSC14["hits"]["hits"])-1)]["_id"]

	for ij in range(11):
		ohneEngMSC14all = es.search(index="temp_zbmath_my",
			body={"_source": ["id"],
			"size": 100000,
		 	"query": {
		   		"bool": {
		     	"must_not": [{ 
		       		"wildcard": {
		     		"reviews.language": "English"
		    		}
		    	}]
		 	}
		 	},
		 	"search_after" : [idTostartwith]
		 	},
			sort = ["id"])
		idTostartwith = ohneEngMSC14all["hits"]["hits"][(len(ohneEngMSC14all["hits"]["hits"])-1)]["_id"]
		print(idTostartwith)
		for everyInner in ohneEngMSC14all["hits"]["hits"]:
			setAllnonenglishIDs.append(everyInner["_id"])

		# listofIDS = list()
		print(len(ohneEngMSC14all["hits"]["hits"]))

	with open('ohneEngIDSall.pkl', 'wb') as fr:
		pickle.dump(setAllnonenglishIDs, fr)

	# for everyEle in ohneEngMSC14["hits"]["hits"]:
	# 	listofIDS.append(everyEle["_id"])

	# print(listofIDS[1200])

# with open('ohneEngIDSall.pkl', 'rb') as fr:
# 	allnonengl = pickle.load(fr)
# 	print(len(set(allnonengl)))

#docsWithoutEngAll()