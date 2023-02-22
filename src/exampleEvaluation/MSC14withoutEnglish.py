import dill as pickle
from elasticsearch import Elasticsearch

es = Elasticsearch()

"""
Allows searcg for ES index with specific MSCs.
Especially important to get documents count per MSCs
"""

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
 	}},
	sort = ["id"])

print(len(ohneEngMSC14["hits"]["hits"]))

listofIDS = list()

for everyEle in ohneEngMSC14["hits"]["hits"]:
	listofIDS.append(everyEle["_id"])

print(listofIDS[1200])

with open('ohneEngIDS.pkl', 'wb') as fr:
	pickle.dump(listofIDS, fr)