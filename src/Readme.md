# Scripts used for creating A Gold Standard Dataset for Recommending Scientific Documents with Mathematical Content

- preProcessing
	- docsPerMSC.py
	- exploratoryAnalysis.py
	- extractMOIs.py
	- extractTOIs.py
	- getAlldocs.py
	- remvShrtdocs.py
-  seedDocSelection
	- reprMSCsel.py
	- workingDset.py
	- captureProb.py
-  exampleEvaluation
	- collectionsRef.py
	- evalRecms.py
	- genRecms.py
	- getDocInfoFromES.py
	- loadDOcsonES.py
	- MSC14withoutEnglish.py
	- recomPairsStat.py
	- reindexProp.txt

## Elasticsearch indexing configuration

- exampleEvaluation
	- reindexProp.txt : 
		- Indexing configurations.
		- Search Analyzers
		- Tokenizers

- Even if you your "whiteSpace" and "onlyAlphanumeric" as your analyzer configuration, ES will directly remove math terms from the dataset.

- For indexing math, follow the anaylzer configuration from the file: reindexProp.txt
	- It will index math expressions as whole tokens (without any preprocessing at all) 