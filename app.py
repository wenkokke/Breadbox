#!/usr/bin/env python

"""
@author: Wen Kokke
"""

import flask
import gensim
import inflect
import json
import nltk
import os
import random
import urllib.request

# set allowed origins
allowed_origins = ['http://127.0.0.1:5000', 'https://127.0.0.1:5000',
                   'http://wenkokke.github.io', 'https://wenkokke.github.io',]

# load app and data
app = flask.Flask(__name__)
data_file = 'GoogleNews-vectors-negative300-SLIM.bin.gz'
model = gensim.models.KeyedVectors.load_word2vec_format(data_file, binary=True)
vocab = list(model.vocab.keys())
inflect = inflect.engine()

@app.route('/')
def hello():
    return flask.render_template('index.html',**new_secret())

@app.route('/guess/<this>/<that>')
def guess(this, that):
    origin = flask.request.headers.get('origin')
    if origin is None or origin in allowed_origins:
        resp = flask.Response(json.dumps({
            'similarity': str(model.wv.similarity(this, that)),
            'a_or_an': inflect.a(that)
        }))
        resp.headers['Access-Control-Allow-Origin'] = origin
        return resp
    return ''

@app.route('/generate/secret')
def generate_secret():
    origin = flask.request.headers.get('origin')
    if origin is None or origin in allowed_origins:
        resp = Response(json(new_secret()))
        resp.headers['Access-Control-Allow-Origin'] = origin
        return resp
    return ''

@app.route('/<path:resource>')
def serveStaticResource(resource):
    return flask.send_from_directory('static/', resource)

def new_secret():
    secret = random.choice(vocab)
    secret_with_article = inflect.a(secret)
    synsets = nltk.corpus.wordnet.synsets(secret)
    definitions = [s.definition() for s in synsets if s.name().startswith(secret+".n")]
    return {
        'secret': secret,
        'secret_with_article': secret_with_article,
        'definitions': definitions,
    }

if __name__ == "__main__":
    PORT = int(os.environ.get('OPENSHIFT_PYTHON_PORT', 8080))
    app.run(host='0.0.0.0', port=PORT)
