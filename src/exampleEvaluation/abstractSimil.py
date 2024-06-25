import os
import csv
import torch
import pickle
from collections import defaultdict
from transformers import AutoTokenizer, AutoModel

"""
This script is with model LLM-embedder but if you want to use other model
Please replace 
"""

INSTRUCTIONS = {
    "qa": {
        "query": "Represent this query for retrieving relevant documents: ",
        "key": "Represent this document for retrieval: ",
    },
}

def getidealrecommendations():
    listDocs = list()
    with open(
        "data/recommendationPairs.csv",
        mode="r",
    ) as csvfile:
        csvFile = csv.reader(csvfile)
        for lines in csvFile:
            IdsandRec = list(filter(None, lines))
            listDocs += IdsandRec[1:]
    return listDocs


def getSEEDIds():
    """
    get seed IDS in a list
    """
    listDocs = list()
    with open(
        "data/recommendationPairs.csv",
        mode="r",
    ) as csvfile:
        csvFile = csv.reader(csvfile)
        for lines in csvFile:
            IdsandRec = list(filter(None, lines))
            listDocs.append(IdsandRec[0])
    return listDocs


def getIDs41():
    filename = "arxMLiv/zbmath_abstracts.csv"
    dataWhole = list()
    with open(filename, "r", encoding="utf-8", errors="ignore") as csvfile:
        csvreader = csv.reader(csvfile)
        first_row = next(csvreader)  # Read the first row
        for eachro in csvreader:
            present14 = False
            for eachmsc in eachro[1].split():
                if "14" == eachmsc[:2]:
                    present14 = True
            if present14:
                dataWhole.append(eachro[0])
    combinedlist = list(set(dataWhole).union(getidealrecommendations()))
    return combinedlist

def getAlltitles(filename):
    """retrurns dict with key as zbMATH ID and value as titles"""
    dataWhole = dict()
    # impIDs = getIDs41() #Only for 14
    with open(filename, "r", encoding="utf-8", errors="ignore") as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for eachro in csvreader:
            dataWhole[eachro[0]] = eachro[1]
    return dataWhole

def genEmbeddingsBatch():
    alltitles = getAlltitles("data/zbMATH_abstracts.csv")
    instruction = INSTRUCTIONS["qa"]
    tokenizer = AutoTokenizer.from_pretrained("BAAI/llm-embedder")
    model = AutoModel.from_pretrained("BAAI/llm-embedder")
    queries = [
        instruction["query"] + alltitles[query] for query in getSEEDIds()
    ]
    query_inputs = tokenizer(
        queries,
        padding=True,
        truncation=True,
        return_tensors="pt",
    )
    for i in range(0, len(alltitles) - 1, 5000):
        print("Doing for batch: ", i)
        keys = [
            instruction["key"] + alltitles[key]
            for key in list(alltitles.keys())[i : i + 5000]
        ]
        key_inputs = tokenizer(
            keys,
            padding=True,
            truncation=True,
            return_tensors="pt",
        )
        with torch.no_grad():
            query_outputs = model(**query_inputs)
            key_outputs = model(**key_inputs)
            query_embeddings = query_outputs.last_hidden_state[:, 0]
            key_embeddings = key_outputs.last_hidden_state[:, 0]
            query_embeddings = torch.nn.functional.normalize(
                query_embeddings,
                p=2,
                dim=1,
            )
            key_embeddings = torch.nn.functional.normalize(
                key_embeddings,
                p=2,
                dim=1,
            )
        similarity = query_embeddings @ key_embeddings.T

        with open("data_ne/abstracts/abs_" + str(i) + "_.pkl", "wb") as f:
            pickle.dump(similarity, f)


def createDictScores(dir_here):
    alltitles = getAlltitles("data/zbMATH_abstracts.csv")
    getAllscores = os.listdir(dir_here)
    allSeeds = getSEEDIds()
    # print(getAllscores)
    seed_to_scores = defaultdict(lambda: list())
    for pick in getAllscores:
        with open(os.path.join(dir_here, pick), "rb") as f:
            scores = pickle.load(f)
        for id_, ele in enumerate(scores):
            seed_to_scores[id_] += ele
    # print(len(seed_to_scores[id_]))
    docIds = list()
    for i in range(0, len(alltitles) - 1, 5000):
        docIds += list(alltitles.keys())[i : i + 5000]
    # print(len(docIds))
    dictSeedRec = dict()
    for seed in seed_to_scores.keys():
        dictOfscores = dict()
        for id_h, eachScore in enumerate(seed_to_scores[seed]):
            dictOfscores = dict()
            for id_h, eachScore in enumerate(seed_to_scores[seed]):
                dictOfscores[docIds[id_h]] = eachScore.item()
        dictSeedRec[allSeeds[seed]] = dictOfscores
    sorted_dict = dict()
    for each_ in dictSeedRec.keys():
        sorted_dict[each_] = sorted(
            dictSeedRec[each_].items(),
            key=lambda x: x[1],
            reverse=True,
        )
    with open("abstracts_LLMemb.pkl", "wb") as f:
        pickle.dump(sorted_dict, f)

createDictScores(
    "evaluation/hybridApproach/data_ne/abstracts",
)