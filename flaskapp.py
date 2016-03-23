"""
Created on Mar 22, 2016

@author: Pepijn Kokke
"""
from composes.semantic_space.space import Space
from composes.similarity.cos       import CosSimilarity
from composes.utils                import io_utils
from flask                         import *
from inflect                       import engine
from json                          import dumps   as json
from nltk.corpus                   import wordnet as wn
from random                        import choice


origins = ['http://127.0.0.1:4000'
           ,'https://127.0.0.1:4000'
           ,'http://pepijnkokke.github.io'
           ,'https://pepijnkokke.github.io']


inflect = engine()
sim = CosSimilarity()
dat = io_utils.load('corpora/composes.pkl')
app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')


@app.route('/')
def index():
    secret              = choice(dat.id2row)
    secret_with_article = inflect.a(secret)
    definitions         = [s.definition() for s in wn.synsets(secret)
                   if s.name().startswith(secret+'.n.')]
    return render_template('index.html'
                           ,secret              = secret
                           ,secret_with_article = secret_with_article
                           ,definitions         = definitions)

@app.route('/guess/<this>/<that>')
def similarity(this, that):
    origin = request.headers.get('origin')
    if origin is None or origin in origins:
        resp = Response(json({
            'similarity' : dat.get_sim(this, that, sim),
            'a_or_an'    : inflect.a(that)
        }))
        resp.headers['Access-Control-Allow-Origin'] = origin
        return resp
    return ''

@app.route('/generate/secret')
def generate_secret():
    origin = request.headers.get('origin')
    if origin is None or origin in origins:
        secret              = choice(dat.id2row)
        secret_with_article = inflect.a(secret)
        definitions         = [s.definition() for s in wn.synsets(secret)
                               if s.name().startswith(secret+'.n.')]
        resp = Response(json({'secret': secret
                              ,'secret_with_article': secret_with_article
                              ,'definitions': definitions}))
        resp.headers['Access-Control-Allow-Origin'] = origin
        return resp
    return ''

@app.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)

@app.route('/test')
def test():
    return "<strong>It's Alive!</strong>"

if __name__ == '__main__':
    app.run()
