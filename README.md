# A Gold Standard Dataset for Recommending Scientific Documents with Mathematical Content

In this repository, we include the first gold standard dataset for recommending scientific documents with mathematical content. Along with the dataset, we provide scripts used to construct the dataset and to run an example evaluation.

## Repository contents

- [Dataset](#Dataset)
- [Preprocessing and Seed documents selection](#Preprocessing-and-Seed-documents-selection)
- [Example use case of dataset](#Example-use-case-of-dataset)

## Dataset

As of Feb-2023, there are 421 recommendation pairs with 80 seed documents.

### 1. Recommendation pairs.

All recommendation pairs are available [in this file](https://github.com/gipplab/MathRecGoldStandData/blob/main/dataset/recommendationPairs.csv) are with their zbMATHOpen_ID. For example: The document with ID:1566951 is ["Noncommutative symmetric algebras of two-sided vector spaces."](https://zbmath.org/?q=an%3A1566951)
Sample recommendation pairs from the curated dataset.


| Seed    | 1st |     2nd  |        3rd |   4th      |  5th       |
|---------|---------|---------|---------|---------|---------|
| 1566951 | 4181495      | 930151  | 5083606 | 1579464 | 6338806 |
| 1363213 | 1445144		 | 1036371 | 6225939 | 2165994 | 1801581 |
| 1308161 | 1356576		 | 4193896 | 5638157 | 5007259 |         |
| 1303018 | 951967		 | 5354085 | 5120555 | 427914  | 224045  |
| 1591097 | 5049067		 | 3867686 | 1758339 | 2136591 |         |


The first column represents the seed documents and subsequent columns ranked recommendations. The recommendations are ranked according to the decreasing order of relevancy.


### 2. Document contents.

Each document's contents such as title, abstract/review/summarry, authors, MSC codes, Full-text link, references, etc are available in [the separate file](https://github.com/gipplab/MathRecGoldStandData/blob/main/dataset/documentContents.csv).

Example document from the file:

| zbMATH_ID | Title                  | Abstract/Review/Summarry                                       | Authors        | Keywords                                  | MSCs             | Full text link                                | References                       |
|-----------|------------------------|----------------------------------------------------------------|----------------|-------------------------------------------|------------------|-----------------------------------------------|----------------------------------|
| 10342     | Maximal contact ...... | The author proves the following theorem: Fix an infinite...... | Cossart V..... | Samuel stratum and desingularization..... | [{code: 14E15... | https://doi.org/10.1215/S0012-7094-91-06303-9 | S. Abhyankar: Resolution of..... |


Additionally, contents from any documents from zbMATH Open can be fetched via [zbMATH Open API](https://oai.zbmath.org/) or available in the [repository](https://zenodo.org/record/6448360#.Y_UmrHbP02w).

## Preprocessing and Seed documents selection

Please install dependencies from [requirements.txt](https://github.com/gipplab/MathRecGoldStandData/blob/main/src/requirements.txt) before running any scripts.

### Preprocessing

The following table provides scripts and its functions/steps involved in preprocessing.

| No. | Functionality/Step                       			| Script      	      |
|-----|-----------------------------------------------------|---------------------|
| 1   | Load all zbMATH Open documents as loocal .txt files | [getAlldocs.py](https://github.com/gipplab/MathRecGoldStandData/blob/main/src/preProcessing/getAlldocs.py)   |
| 2   | Remove short/irrelevant documents        			| [remvShrtdocs.py](https://github.com/gipplab/MathRecGoldStandData/blob/main/src/preProcessing/remvShrtdocs.py) |
| 3   | Extract TOIs and remove Non-English documents       | [extractTOIs.py](https://github.com/gipplab/MathRecGoldStandData/blob/main/src/preProcessing/extractTOIs.py)  |
| 4   | Convert LaTeX to MathML and extract MOIs 			| [extractMOIs.py](https://github.com/gipplab/MathRecGoldStandData/blob/main/src/preProcessing/extractMOIs.py)  |
| 5   | Discipline-wise documents                			| [docsPerMSC.py](https://github.com/gipplab/MathRecGoldStandData/blob/main/src/preProcessing/docsPerMSC.py)   | 


### Seed documents selection

The representative seed documents selection follows a four step procedure. Each step and its corresponding scripts are available in the following table.

| Step No. | Name                              | Script               |
|----------|-----------------------------------|----------------------|
| 1        | Mathematical discipline selection | [reprMSCsel.py](https://github.com/gipplab/MathRecGoldStandData/blob/main/src/seedDocSelection/reprMSCsel.py)    |
| 2        | Working dataset creation          | [workingDset.py](https://github.com/gipplab/MathRecGoldStandData/blob/main/src/seedDocSelection/workingDset.py)   |
| 3        | Capture probability calculation   | [captureProb.py](https://github.com/gipplab/MathRecGoldStandData/blob/main/src/seedDocSelection/captureProb.py)   |
| 4        | Final seeds selection             | [finalSeedsSel.py](https://github.com/gipplab/MathRecGoldStandData/blob/main/src/seedDocSelection/finalSeedsSel.py) |


## Example use case of dataset

We demonstrate an example evaluation of recommendation approaches with our dataset.
For generating recommendations, we consider two document collections, i.e., zbMATH Open and Algebraic Geometry.
These collections contain 4.5 million documents and 86 thousand documents, respectively.
To rank recommendations, we use the BM25 algorithm (a modified TF-IDF scheme) with cosine similarity provided by the default search capability of [Elasticsearch(ES)](https://www.elastic.co/).
We use two document elements for comparison, text and math expressions.

1. Versions used
	1. Elasticsearch: [7.9.3](https://www.elastic.co/jp/downloads/past-releases/elasticsearch-7-9-3)
	2. Kibana (only for testing purposes): [7.9.3](https://www.elastic.co/downloads/past-releases/kibana-7-9-3)

The following table includes scripts and its corresponding functinality for perfoming example evaluation. Please adjust the Elasticsearch configurations based on your used infrastrucure. Our scripts include experiments sufficient to run on a local system. However, we expect that at least 40 GB of free space is available for Elasticsearch and Kibana.


| No. | Functionality/Step                             | Script                |
|-----|------------------------------------------------|-----------------------|
| 1   | Load zbMATH Open documents on ES               | [loadDOcsonES.py](https://github.com/gipplab/MathRecGoldStandData/blob/main/src/exampleEvaluation/loadDOcsonES.py)   |
| 2   | indexing Configuration (text and text + Math ) | [collectionsRef.py](https://github.com/gipplab/MathRecGoldStandData/blob/main/src/exampleEvaluation/collectionsRef.py) |
| 3   | Generate recommendations                       | [genRecms.py](https://github.com/gipplab/MathRecGoldStandData/blob/main/src/exampleEvaluation/genRecms.py)       |
| 4   | Evaluate recommendation                        | [evalRecms.py](https://github.com/gipplab/MathRecGoldStandData/blob/main/src/exampleEvaluation/evalRecms.py)      |

The above mentioned scripts are not all the scripts. Please refer to the [seed documents selection](https://github.com/gipplab/MathRecGoldStandData/tree/main/src/) folder for more detaila.


## License 

Legal restrictions and copyright: The zbMATH Open data is subject to the Terms and Conditions for the zbMATH Open API Service of FIZ Karlsruhe – Leibniz-Institut für Informationsinfrastruktur GmbH. Content generated by zbMATH Open, such as reviews, classifications, software, or author disambiguation data, are distributed under CC-BY-SA 4.0. This defines the license for the whole dataset, which also contains non-copyrighted bibliographic metadata and reference data derived from I4OSC (CC0).