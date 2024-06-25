import json
import random
import math
from collections import defaultdict

def tokBySize(represToks):
    tokWTsize = defaultdict(lambda: dict())
    for each_tok in represToks.keys():
        tokWTsize[len(each_tok)][each_tok] = represToks[each_tok]
    
    tokWTsizePro = defaultdict(lambda: dict())
    for eachSize in tokWTsize.keys():
        if eachSize not in [0]:
            tokWTsizePro[eachSize] = tokWTsize[eachSize]
    return tokWTsizePro

def overallFreq(keysize, mainDict, ovrlTokcnt):
    allWordodSize = mainDict[keysize]
    ttlOccKey = 0
    for everyWord in allWordodSize.keys():
        ttlOccKey += allWordodSize[everyWord]
    return ttlOccKey / ovrlTokcnt

def granularProb(dictWithTokVal, sml_n, cap_N, ovrlTokcn):
    ttlTokSize_i = 0
    for uniqwrds in dictWithTokVal.keys():
        ttlTokSize_i += dictWithTokVal[uniqwrds]
    
    probSumm = 0
    for uniqwrds in dictWithTokVal.keys():
        a_ij = dictWithTokVal[uniqwrds] / ttlTokSize_i
        f_i = dictWithTokVal[uniqwrds] / ovrlTokcn
        lambda_i = f_i / (cap_N / sml_n)
        prob_m = 1 - math.exp(-lambda_i)
        probSumm += a_ij * prob_m
    
    return probSumm

def captureProbab(sampleSize, smllTolrgTok):
    n = sampleSize
    N = 22892  # Our working dataset size
    ovrlTokcnt = 0
    for keySize in smllTolrgTok.keys():
        for inKeys in smllTolrgTok[keySize].keys():
            ovrlTokcnt += smllTolrgTok[keySize][inKeys]
    
    numrTr = 0
    denTr = 0
    for keySize in smllTolrgTok.keys():
        if keySize > 4:
            b_j = overallFreq(keySize, smllTolrgTok, ovrlTokcnt)
            denTr += b_j
            P_J = granularProb(smllTolrgTok[keySize], n, N, ovrlTokcnt)
            numrTr += b_j * P_J
    
    aggcapProb = numrTr / denTr
    return aggcapProb

def select_random_documents(input_json_file, sample_size):
    with open(input_json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    selected_documents = random.sample(list(data.keys()), sample_size)
    
    represToks = {doc_id: data[doc_id] for doc_id in selected_documents}
    
    smllTolrgTok = tokBySize(represToks)
    capture_probability = captureProbab(sample_size, smllTolrgTok)
    
    return selected_documents, capture_probability

if __name__ == "__main__":
    input_json_file = input("Enter the path to the input JSON file: ")
    sample_size = int(input("Enter the sample size: "))
    
    selected_documents, capture_probability = select_random_documents(input_json_file, sample_size)
    
    print(f"Selected Documents: {selected_documents}")
    print(f"Capture Probability: {capture_probability}")