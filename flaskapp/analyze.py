"""
Reads txt files of all papers and computes tfidf vectors for all papers.
Dumps results to file tfidf.p
"""
import os
import pickle
from random import shuffle, seed

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import Pipeline

from utils import Config, safe_pickle_dump

seed(1337)

# read database
db = pickle.load(open(Config.db_path, 'rb'))
trainedpapers = {} # db with papers that were used in training

# read all text files for all papers into memory
txt_paths, pids = [], []
n = 0
for pid,j in db.items():
    n += 1
    idvv = '%sv%d' % (j['_rawid'], j['_version'])
    txt_path = os.path.join('data', 'txt', idvv) + '.pdf.txt'
    if os.path.isfile(txt_path): # some pdfs dont translate to txt
        with open(txt_path, 'r') as f:
            txt = f.read()
            if len(txt) > 1000 and len(txt) < 500000: # 500K is VERY conservative upper bound
                txt_paths.append(txt_path) # todo later: maybe filter or something some of them
                pids.append(idvv)
                print("read %d/%d (%s) with %d chars" % (n, len(db), idvv, len(txt)))
                trainedpapers[pid] = j
            else:
                print("skipped %d/%d (%s) with %d chars: suspicious!" % (n, len(db), idvv, len(txt)))
    else:
        print("could not find %s in txt folder." % (txt_path, ))
print("in total read in %d text files out of %d db entries." % (len(txt_paths), len(db)))
print("writing ", Config.trained_path)
safe_pickle_dump(trainedpapers, Config.trained_path)

# compute tfidf vectors with scikits
vectorizer = TfidfVectorizer(input='content', 
        encoding='utf-8', decode_error='replace', strip_accents='unicode', 
        lowercase=True, analyzer='word', stop_words='english', 
        token_pattern=r'(?u)\b[a-zA-Z_][a-zA-Z0-9_]+\b', 
        norm='l2', use_idf=True, smooth_idf=True, sublinear_tf=True,
        max_df=1.0, min_df=1)

# build an SVD model, n_components = 100 is chosen in random
svd_model = TruncatedSVD(n_components=100, 
                         algorithm='randomized',
                         n_iter=10, random_state=42)

# create an iterator object to conserve memory
def make_corpus(paths):
  for p in paths:
    with open(p, 'r') as f:
      txt = f.read()
    yield txt

# train
print("training on %d documents..." % (len(txt_paths), ))
train_corpus = make_corpus(txt_paths)
svd_transformer = Pipeline([('tfidf', vectorizer), 
                            ('svd', svd_model)])
svd_matrix = svd_transformer.fit_transform(train_corpus)

print("writing lsi", Config.lsi_path)
safe_pickle_dump(svd_matrix, Config.lsi_path)

print("writing svd transformer", Config.transformer_path)
safe_pickle_dump(svd_transformer, Config.transformer_path)

# writing lighter metadata information into a separate (smaller) file
out = {}
out['pids'] = pids # a full idvv string (id and version number)
out['ptoi'] = { x:i for i,x in enumerate(pids) } # pid to ix in X mapping

print("writing", Config.meta_path)
safe_pickle_dump(out, Config.meta_path)
