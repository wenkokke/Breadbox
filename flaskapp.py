from composes.semantic_space.space import Space
from composes.similarity.cos       import CosSimilarity
from composes.utils                import io_utils
from flask                         import Flask
from random                        import choice


dat = io_utils.load('data.pkl')
app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')


@app.route('/')
def index():
    return "<strong>It's Alive!</strong>"


@app.route('/generate/secret')
def generate_secret():
    return choice(dat.id2row)


if __name__ == '__main__':
    app.run()
