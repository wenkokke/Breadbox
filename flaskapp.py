from composes.semantic_space.space import Space
from composes.similarity.cos       import CosSimilarity
from composes.utils                import io_utils
from flask                         import Flask
from random                        import choice
from nltk.corpus                   import wordnet as wn

dat = io_utils.load('data.pkl')
app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')


@app.route('/')
def index():
    return "<strong>It's Alive!</strong>"


@app.route('/generate/secret')
def generate_secret():
    secret = choice(dat.id2row)
    output = [secret]
    for synset in wn.synsets(secret):
        if synset.name().startswith(secret+'.n.'):
            output.append("It's " + synset.definition() + ".")
    return '<br />'.join(output)


if __name__ == '__main__':
    app.run()
