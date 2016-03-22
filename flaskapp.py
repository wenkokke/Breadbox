"""
Created on Mar 22, 2016

@author: Pepijn Kokke
"""
from composes.semantic_space.space import Space
from composes.similarity.cos       import CosSimilarity
from composes.utils                import io_utils
from flask                         import Flask
from json                          import dumps as json
from random                        import choice
from nltk.corpus                   import wordnet as wn
from nltk.corpus                   import cmudict as cm


sim = CosSimilarity()
dat = io_utils.load('data.pkl')
app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')


@app.route('/generate/secret')
def generate_secret():
    return json(choice(dat.id2row))


@app.route('/definitions/<this>')
def definitions(this):
    return json([s.definition() for s in wn.synsets(this)
                  if s.name().startswith(this+'.n.')])


@app.route('/similarity/<this>/<that>')
def similarity(this, that):
    return json(dat.get_sim(this, that, sim))


@app.route('/startswith/vowel/<this>')
def startswith_vowel(this):
    for syllables in cm.dict().get(this,[]):
        return json(syllables[0][-1].isdigit())
    return json(False)


@app.route('/test')
def index():
    return "<strong>It's Alive!</strong>"


if __name__ == '__main__':
    app.run()
