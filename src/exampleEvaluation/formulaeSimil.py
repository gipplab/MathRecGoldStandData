import os
import re
import csv
import jsonlines

def getidealRecommendations():
    """
    get Ideal Recmnds in a list
    """
    listDocs = dict()
    with open(
        "data/recommendationPairs.csv",
        mode="r",
    ) as csvfile:
        csvFile = csv.reader(csvfile)
        for lines in csvFile:
            IdsandRec = list(filter(None, lines))
            listDocs[IdsandRec[0]] = IdsandRec[1:]
    return listDocs


def checkFirstEntry(files_location):
    listredo = list()
    allFiles = os.listdir(files_location)
    for fls in allFiles:
        try:
            fileName = fls.split(".")[0]
            with open(os.path.join(files_location, fls), "r") as txtF:
                txtFile = txtF.read()
            lines = txtFile.split("\n")
            matches = re.findall(r"'(.*?)'", lines[0].split(" ")[1])
            if fileName != matches[0]:
                listredo.append(fileName)
        except:
            print("went wrong for: ", fls)
    print(listredo)


def cleanDPRscores(prev_dprScores):
    """
    clean DPR score dict becuase the doc id are output as tensors
    output: dict with key as seed ID and values as dict with key as doc ID andvalues  scores
    """
    finalScores = dict()
    for eachD in prev_dprScores.keys():
        localDict = dict()
        for eachK in prev_dprScores[eachD].keys():
            localDict[re.findall(r"'(.*?)'", eachK)[0]] = prev_dprScores[
                eachD
            ][eachK]
        finalScores[eachD] = localDict
    return finalScores


def extractScores(scoresLocation):
    """
    input: scoresLocation: location where all .run files are stored
    output: dict with key as doc ID and values as a list with doc id and similarity scores
    """
    allFiles = os.listdir(scoresLocation)
    docandRetrivdc = dict()
    for fls in allFiles:
        fileName = fls.split(".")[0]  # removing .run for doc ID
        localDict = dict()
        with open(os.path.join(scoresLocation, fls), "r") as txtF:
            txtFile = txtF.read()
        lines = txtFile.split("\n")
        for lin in lines:
            eles = lin.split(" ")
            if eles != [""]:
                localDict[eles[2]] = eles[4]
            # print(eles[2], eles[4])
        docandRetrivdc[fileName] = localDict
    return docandRetrivdc


def completeScores():
    a0scores = extractScores(
        "data/mabowdor/recsys/pya0",
    )
    dprscores = cleanDPRscores(
        extractScores("data/mabowdor/recsys/dpr"),
    )
    aos = dict()
    for eachD in dprscores.keys():
        absDocids = list(
            set(dprscores[eachD].keys()) - set(a0scores[eachD].keys()),
        )
        aoLow = sorted(a0scores[eachD].values())
        for absID in absDocids:
            a0scores[eachD][absID] = str(float(aoLow[0]) - 1)
        aos[eachD] = a0scores[eachD]
        # print(len(aos[eachD]))
        # break
    dps = dict()
    for eachD in a0scores.keys():
        absDocids = list(
            set(a0scores[eachD].keys()) - set(dprscores[eachD].keys()),
        )
        dprLow = sorted(dprscores[eachD].values())
        for absID in absDocids:
            dprscores[eachD][absID] = str(float(dprLow[0]) - 1)
        dps[eachD] = dprscores[eachD]
        # print(len(dps[eachD]))
        # break
    return aos, dps


def combinedScores():
    """
    input: None
    output: dict with key as seeed ID and top 11 retrievd results from MABOWDOR
    """
    resultsdict = {"seed": None, "idealRcmnds": None, "baselineRcmnds": None}
    allScores = completeScores()
    a0 = allScores[0]
    dpr = allScores[1]
    print(len(a0), len(dpr))
    # sys.exit(0)
    combinedScores = dict()
    for eachK in a0.keys():  # either dpr or a0, can loop through any
        incomb = dict()
        for innerSc in a0[eachK].keys():
            # incomb[innerSc] = str((float(a0[eachK][innerSc]) + float(dpr[eachK][innerSc]))/2)
            incomb[innerSc] = str(float(dpr[eachK][innerSc]))
        # print(len(a0[eachK]),len(dpr[eachK]))
        combinedScores[eachK] = incomb
        # sys.exit(0)
    with jsonlines.open("rslts_mabowDor_dpr.jsonl", mode="w") as writer:
        seed_idlrecmnds = getidealRecommendations()
        for ea in combinedScores.keys():
            baselinercmnds = dict()
            sortedH = sorted(
                combinedScores[ea].items(),
                key=lambda x: x[1],
                reverse=True,
            )[:11]
            for id_, pot_rcmnds in enumerate(sortedH):
                baselinercmnds[str(id_)] = [int(pot_rcmnds[0]), pot_rcmnds[1]]
            # print(ea, sortedH)
            resultsdict["seed"] = ea
            resultsdict["idealRcmnds"] = seed_idlrecmnds[ea]
            resultsdict["baselineRcmnds"] = baselinercmnds
            writer.write(resultsdict)


combinedScores()
# checkFirstEntry("mabowdor/recsys/dpr")