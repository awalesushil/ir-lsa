
# Information Retrieval System using Latent Semantic Indexing

To run this project do the following.

## Download Data

The project uses Machine Learning papers downloaded from arxiv.org using its API.

1. Run fetch_papers.py - Downloads meta information of papers from the API
2. Run download_papers.py - Downloads the actual papers for the corpus
3. Run pdf_to_txt.py - Converts pdf into text file for fitting into the LSA model
   
*Note: The above code does not belong to me. It is taken from https://github.com/karpathy/arxiv-sanity-preserver*

## Train Model

4. Run analyze.py - Train the LSA model using the text corpus

## Running the application

5. export set FLASK_APP=webapp
6. cd flaskapp
7. python -m flask run
