from flask import Flask, jsonify
from flask import render_template, request
from datetime import datetime
from . import app

#from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import pairwise_distances

import pickle
import numpy as np
np.set_printoptions(threshold=np.nan, precision=4)

from . import utils

import pprint
import time

svd_matrix = pickle.load(open(utils.Config.lsi_path, 'rb'))
svd_transformer = pickle.load(open(utils.Config.transformer_path, 'rb'))
trainedpapers = pickle.load(open(utils.Config.trained_path, 'rb'))

def papers_search(qraw, svd_matrix, svd_transformer, trainedpapers):
    
    query_vector = svd_transformer.transform([qraw.lower()])

    distance_matrix = distance_matrix = pairwise_distances(query_vector, 
                                     svd_matrix, 
                                     metric='cosine', 
                                     n_jobs=-1)
    
    index = 0    
    for pid, p in trainedpapers.items():
        p['cosine_distance'] = distance_matrix[0][index]
        index += 1

    ranked_papers = sorted(trainedpapers.items(), key=lambda x: (x[1]['cosine_distance']))
    return ranked_papers

@app.route("/")
def home():
    papers = sorted(trainedpapers.items(), key=lambda x: (x[1]['published']))
    return render_template("home.html", papers = papers[0:9])

@app.route("/search", methods = ['GET', 'POST'])
def result():
    q = request.args.get('query') # get the search request
    tic = time.time()
    ranked_papers = papers_search(q, svd_matrix, svd_transformer, trainedpapers) # perform the query and get sorted documents
    toc = time.time()
    queried_time = "%.4f" % (toc-tic)
    utils.safe_pickle_dump(ranked_papers, utils.Config.ranked_path)
    return render_template("home.html", papers = ranked_papers[:9], search_query = q, query_time = queried_time)

@app.route("/addpapers", methods = ['GET', 'POST'])
def addpapers():
    iteration = int(request.args.get('iteration'))
    page = request.args.get('page')
    iteration = iteration * 10
    if page == '/search':
        papers = list(pickle.load(open(utils.Config.ranked_path, 'rb')))
        #papers = sorted(ranked_papers.items(), key=lambda x: (x[1]['cosine_distance']))
    else:
        papers = sorted(trainedpapers.items(), key=lambda x: (x[1]['published']))
    
    return jsonify(papers[iteration:iteration+9])