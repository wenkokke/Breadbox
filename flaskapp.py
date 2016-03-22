from composes.semantic_space.space import Space
from composes.similarity.cos       import CosSimilarity
from composes.utils                import io_utils
from flask                         import Flask
from random                        import choice
from nltk.corpus                   import wordnet as wn
from nltk.corpus                   import cmudict as cm

sim = CosSimilarity()
dat = io_utils.load('data.pkl')
app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')


@app.route('/generate/secret')
def generate_secret():
    secret = choice(dat.id2row)
    output = [secret]
    for synset in wn.synsets(secret):
        if synset.name().startswith(secret+'.n.'):
            output.append("It's " + synset.definition() + ".")
    return '<br />'.join(output)


@app.route('/similarity/<this>/<that>')
def similarity(this, that):
    return str(dat.get_sim(this, that, sim))


@app.route('/startswith/vowel/<this>')
def startswith_vowel(this):
    for syllables in cm.dict().get(this,[]):
        return str(syllables[0][-1].isdigit())
    return str(False)


@app.route('/test')
def index():
    return "<strong>It's Alive!</strong>"


if __name__ == '__main__':
    app.run()
