import os
import csv
import torch
import pickle
from collections import defaultdict
from transformers import AutoTokenizer, AutoModel

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

def getDocandRefstyle():
    dictRef = dict()
    filename = "data/references_withIDs.csv" #File with zbMATHId and and document in the refrence format, can be obtained trhough zbMATHOpen API
    with open(filename, "r", encoding="utf-8", errors="ignore") as csvfile:
        csvreader = csv.reader(csvfile)
        first_row = next(csvreader)  # Read the first row
        for eachro in csvreader:
            dictRef[eachro[2]] = eachro[1]
    return dictRef

def getDocID_to_zbl():
    dictRef = dict()
    #following file is the mapping og internal IDs to ZBLIds, can be obtained through zbMATHOPen API
    with open(
        "data/zbMATH_id_to_ZBL.csv",
        mode="r",
    ) as csvfile:
        csvFile = csv.reader(csvfile)
        next(csvFile)
        for lines in csvFile:
            dictRef[lines[0]] = lines[1]
    zbl_to_ids = {y: x for x, y in dictRef.items()}
    return dictRef, zbl_to_ids

def getAllReferences():
    """Combine refrences in ZBL and and normal format"""
    file_zblcit = "data/math_citation.csv" # Both files can be obtained throuhg zbMATHOpen API
    file_ref = "data/references_withIDs.csv"
    idToZBLcit_o = dict()
    with open(file_zblcit, "r", encoding="utf-8", errors="ignore") as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for eachro in csvreader:
            if eachro[1] != "":
                idToZBLcit_o[eachro[0]] = eachro[1]
    idToZBLcit_re = dict()
    for eachD in idToZBLcit_o.keys():
        temp_c = idToZBLcit_o[eachD].split(";")
        temp_cn = list()
        for eachE in temp_c:
            ele_n = eachE.split(" ")
            if "Zbl" in ele_n:
                ele_n = "".join(ele_n)
                ele_n = ele_n.split("Zbl")[1]
                temp_cn.append(ele_n)
            elif "JFM" in ele_n:
                ele_n = "".join(ele_n)
                ele_n = ele_n.split("JFM")[1]
                temp_cn.append(ele_n)
            elif "ERAM" in ele_n:
                ele_n = "".join(ele_n)
                ele_n = ele_n.split("ERAM")[1]
                temp_cn.append(ele_n)
            else:
                # some IDs start woth "JM" or no identifier or just weird latex form.
                # Upon manually checking these documents had no to very little dataa zbMATH Open
                # Hence ignored for now
                continue
        idToZBLcit_re[eachD] = temp_cn
    idToRefrences_o = defaultdict(lambda: list())
    with open(file_ref, "r", encoding="utf-8", errors="ignore") as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for eachro in csvreader:
            if eachro[2] != "":
                idToRefrences_o[eachro[0]].append([eachro[1], eachro[2]])
    getExistingDEtoRefStyle = getDocandRefstyle()
    for eachID in idToZBLcit_re.keys():
        if eachID in idToRefrences_o.keys():
            listOfpresentZBL = [ele[1] for ele in idToRefrences_o[eachID]]
            for eachZBL in idToZBLcit_re[eachID]:
                if eachZBL not in listOfpresentZBL:
                    if eachZBL in getExistingDEtoRefStyle.keys():
                        idToRefrences_o[eachID].append(
                            [getExistingDEtoRefStyle[eachZBL], eachZBL],
                        )
        else:
            for eachZBL in idToZBLcit_re[eachID]:
                if eachZBL in getExistingDEtoRefStyle.keys():
                    idToRefrences_o[eachID].append(
                        [getExistingDEtoRefStyle[eachZBL], eachZBL],
                    )
    return idToRefrences_o

def getRefSimilarity():
    id_toRefrences = getAllReferences()
    zbl_to_ids, ids_to_zbl = getDocID_to_zbl()
    seed_references = dict()
    references_toseeds = defaultdict(lambda: list())
    seed_ids = getSEEDIds()
    for eachId in id_toRefrences.keys():
        if eachId in seed_ids:
            seed_references[ids_to_zbl[eachId]] = id_toRefrences[eachId]
    getDocref = getDocandRefstyle()
    print("Initial seed ref len: ", len(seed_references))
    for eachId in id_toRefrences.keys():
        for inter in id_toRefrences[eachId]:
            try:
                if zbl_to_ids[inter[1]] in seed_ids:
                    references_toseeds[inter[1]].append(
                        [getDocref[ids_to_zbl[eachId]], eachId],
                    )
            except:
                continue
                # some ZBL Ids are DE Ids (mistakes)
    print("Initial re seed len: ", len(references_toseeds))
    return seed_references, references_toseeds

getRefSimilarity()