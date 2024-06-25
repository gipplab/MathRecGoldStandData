import os
import math
from collections import defaultdict
import pickle

def tokBySize():
    """
    Output: Dictionary with keys as Token lengths and values with a
    dictionary with keys as actual tokens and its frequency.
    """
    tokWTsize = defaultdict(lambda: dict())
    represToks = loadRepresenToks()
    for each_tok in represToks.keys():
        tokWTsize[len(each_tok)][each_tok] = represToks[each_tok]
    
    tokWTsizePro = defaultdict(lambda: dict())
    for eachSize in tokWTsize.keys():
        if eachSize not in [0]:
            tokWTsizePro[eachSize] = tokWTsize[eachSize]
    return tokWTsizePro

def countOftotalTokens():
    preprocessedToks = tokBySize()
    countOftokens = 0
    for keySize in preprocessedToks.keys():
        for inKeys in preprocessedToks[keySize].keys():
            countOftokens += 1
    return countOftokens

def overallFreq(keysize, mainDict, ovrlTokcnt):
    """
    Gives output b_j
    """
    allWordodSize = mainDict[keysize]
    ttlOccKey = 0
    for everyWord in allWordodSize.keys():
        ttlOccKey += allWordodSize[everyWord]
    return ttlOccKey / ovrlTokcnt

def granularProb(dictWithTokVal, sml_n, cap_N, ovrlTokcn):
    """
    Given output P_j
    """
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

if __name__ == "__main__":
    print("Agg capture Prob with 8000 docs: ", captureProbab(8000, tokBySize()))
