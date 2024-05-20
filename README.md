# Towards Better STEM Recommendations: A Gold-Standard Dataset with Math Content

This repository includes the first gold standard dataset for recommending scientific research articles with mathematical content. Along with the dataset, we provide scripts used to construct the dataset and to run an example evaluation.


## Overview of the repo

- dataset : Contains recommendations pairs and their contents. (For the content of each file and descrption, please refer to the "dataset" folder)
- src: Contains python scripts required to come up with the representative seed articles. Additionally, scripts required to use the dataset for evaluating a recommendation system approach. (For the content of each file and descrption, please refer to the "dataset" folder)

## Main contents of the repository

- [Dataset](#Dataset)
- [Example use case of dataset](#Example-use-case-of-dataset)
- [Seed documents Creation](#Preprocessing-and-Seed-documents-selection)

## Dataset

As of April-2023, there are 421 recommendation pairs with 80 seed research articles.

### 1. Recommendation pairs.

All recommendation pairs are available "dataset/recommendationPairs.csv" are with their zbMATHOpen_ID. For example: The research article with ID:1566951 is ["Noncommutative symmetric algebras of two-sided vector spaces."](https://zbmath.org/?q=an%3A1566951)
Sample recommendation pairs from the curated dataset.


| Seed    | 1st recommendation |     2nd recommendation  | 3rd recommendation |   4th recommendation  |  5th   recommendation|
|---------|---------|---------|---------|---------|---------|
| 1566951 | 4181495      | 930151  | 5083606 | 1579464 | 6338806 |
| 1363213 | 1445144		 | 1036371 | 6225939 | 2165994 | 1801581 |
| 1308161 | 1356576		 | 4193896 | 5638157 | 5007259 |         |
| 1303018 | 951967		 | 5354085 | 5120555 | 427914  | 224045  |
| 1591097 | 5049067		 | 3867686 | 1758339 | 2136591 |         |


The first column represents the seed research articles and subsequent columns ranked recommendations. The recommendations are ranked according to the decreasing order of relevancy. In order to find research articles manually in zbMATH Open, search at "https://zbmath.org/" with the prefix an (for example: "an:1566951") or via URL requests directly given the search query with “an:” prefix. For example: https://zbmath.org/?q=an%3A1566951 where %3A is the URL encoding of the colon :


### 2. Document contents.

Each research article's contents such as title, abstract/review/summarry, authors, MSC codes, Full-text link, references, etc are available in dataset/documentContents.csv.

Example research article from the file:

| zbMATH_ID | Title                  | Abstract/Review/Summarry                                       | Authors        | Keywords                                  | MSCs             | Full text link                                | References                       |
|-----------|------------------------|----------------------------------------------------------------|----------------|-------------------------------------------|------------------|-----------------------------------------------|----------------------------------|
| 10342     | Maximal contact ...... | The author proves the following theorem: Fix an infinite...... | Cossart V..... | Samuel stratum and desingularization..... | [{code: 14E15... | https://doi.org/10.1215/S0012-7094-91-06303-9 | S. Abhyankar: Resolution of..... |


Additionally, contents from any research article from zbMATH Open can be fetched via [zbMATH Open API](https://oai.zbmath.org/) directly downloaded from the official repository on zenodo [repository](https://zenodo.org/record/6448360#.Y_UmrHbP02w).

## Example use case of dataset

We demonstrate an example evaluation of recommendation approaches with our dataset. For generating recommendations, we consider zbMATH Open collection. The collection contain 4.5 million documents. To rank recommendations, first we use the BM25 algorithm (a modified TF-IDF scheme) with cosine similarity provided by the default search capability of [Elasticsearch(ES)](https://www.elastic.co/).Second, we utlize language models to generate embeddings and then use cosine similarity to get relevant recommendations.

1. Elasticsearch Versions used
	1. Elasticsearch: [7.9.3](https://www.elastic.co/jp/downloads/past-releases/elasticsearch-7-9-3)
	2. Kibana (only for testing purposes, not neede to run evaluation): [7.9.3](https://www.elastic.co/downloads/past-releases/kibana-7-9-3)

The following table includes scripts and its corresponding functinality for perfoming example evaluation. Our scripts include experiments sufficient to run on a local system. However, we expect that at least 20 GB of free space is available for Elasticsearch.


| No. | Functionality/Step                             | Script                |
|-----|------------------------------------------------|-----------------------|
| 1   | Load zbMATH Open documents on ES               | src/exampleEvaluation/loadDOcsonES.py   |
| 2   | indexing Configuration (text and text + Math ) | src/exampleEvaluation/collectionsRef.py |
| 3   | Generate recommendations                       | src/exampleEvaluation/genRecms.py       |
| 4   | Evaluate recommendation                        | src/exampleEvaluation/evalRecms.py      |
| 5   | Generate embeddings and calculate cosine similarity to generate recommendations | src/baseline/langModelEval.py  |

The above mentioned scripts are not all the scripts. Please refer to the "main/src/" folder for more detaila.

### Example recommendation generation

#### Make sure elasticsearch cluster is running

python src/exampleEvaluation/genRecms.py 


## Seed documents Creation

Here we mention the scripts to get the representative seeds from the zbMATH Open. Note: These steps are not required if you directly want to use the dataset. Please refer to the "Example use case of the dataset" below for information regarding utilizing dataset for evaluation.

Please install dependencies from src/requirements.txt before running any scripts.

### virtual environment
`python3 -m venv recseedsel` (More on creating [virtual environment](https://docs.python.org/3/library/venv.html))
`source recseedsel/bin/activate` ([activate](https://docs.python.org/3/tutorial/venv.html#:~:text=Once%20you%E2%80%99ve%20created%20a%20virtual%20environment%2C%20you%20may%20activate%20it.) virtual environment)

### install dependencies
`pip install -r src/requirements.txt`

### 1. Preprocessing

The following table provides scripts and its functions/steps involved in preprocessing. The preprocessing steps are only required to calculate the representative seed research article.

| No. | Functionality/Step                       			| Script      	      |
|-----|-----------------------------------------------------|---------------------|
| 1   | Load all zbMATH Open documents as local .txt files | src/preProcessing/getAlldocs.py   |
| 2   | Remove short/irrelevant documents        			| src/preProcessing/remvShrtdocs.py |
| 3   | Extract TOIs and remove Non-English documents       | src/preProcessing/extractTOIs.py  |
| 4   | Convert LaTeX to MathML and extract MOIs 			| src/preProcessing/extractMOIs.py  |
| 5   | Discipline-wise documents                			| src/preProcessing/docsPerMSC.py   | 


### 2. Seed documents selection

The representative seed documents selection follows a four step procedure. Each step and its corresponding scripts are available in the following table.

| Step No. | Name                              | Script               |
|----------|-----------------------------------|----------------------|
| 1        | Mathematical discipline selection | src/seedDocSelection/reprMSCsel.py    |
| 2        | Working dataset creation          | src/seedDocSelection/workingDset.py   |
| 3        | Capture probability calculation   | src/seedDocSelection/captureProb.py   |
| 4        | Final seeds selection             | src/seedDocSelection/finalSeedsSel.py |


## License 

CC-BY-SA 4.0. This defines the license for the whole dataset, which also contains non-copyrighted bibliographic metadata and reference data derived from I4OSC (CC0).
