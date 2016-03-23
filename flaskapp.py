"""
Created on Mar 22, 2016

@author: Pepijn Kokke
"""
from composes.semantic_space.space import Space
from composes.similarity.cos       import CosSimilarity
from composes.utils                import io_utils
from flask                         import Flask, render_template, send_from_directory
from inflect                       import engine  as ie
from json                          import dumps   as json
from nltk.corpus                   import wordnet as wn
from random                        import choice


inf = ie()
sim = CosSimilarity()
dat = io_utils.load('corpora/composes.pkl')
app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')


@app.route('/')
def index():
    secret              = choice(dat.id2row)
    secret_with_article = inf.a(secret)
    definitions         = [s.definition() for s in wn.synsets(secret)
                   if s.name().startswith(secret+'.n.')]
    return render_template('index.html'
                           ,secret              = secret
                           ,secret_with_article = secret_with_article
                           ,definitions         = definitions)

@app.route('/guess/<this>/<that>')
def similarity(this, that):
    return json({
        'similarity' : dat.get_sim(this, that, sim),
        'a_or_an'    : inf.a(that)
    })

@app.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)

@app.route('/test')
def test():
    return "<strong>It's Alive!</strong>"

if __name__ == '__main__':
    app.run()
