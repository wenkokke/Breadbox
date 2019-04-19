from setuptools                 import setup, find_packages
from setuptools.command.install import install as _install

class Install(_install):
    def run(self):
        if not self.dry_run:
            _install.do_egg_install(self)

            # download 'wordnet'
            import nltk
            nltk.download('wordnet')

            # create 'data' directory
            import os
            if not os.path.isdir('data'):
                os.mkdir('data')

            # download 'GoogleNews SLIM'
            from urllib.request import urlopen
            url = "https://github.com/eyaler/word2vec-slim/raw/master/GoogleNews-vectors-negative300-SLIM.bin.gz"
            resp = urlopen(url)
            CHUNK = 16 * 1024
            with open('data/GoogleNews-vectors-negative300-SLIM.bin.gz','wb') as f:
                while True:
                    chunk = resp.read(CHUNK)
                    if not chunk:
                        break
                    f.write(chunk)

setup(name='Breadbox',
      version          ='2.0',
      description      ='Implementation of "Breadbox" or "Plenty Questions".',
      author           ='Wen Kokke',
      author_email     ='wen.kokke@gmail.com',
      url              ='http://www.python.org/sigs/distutils-sig/',
      cmdclass         ={'install': Install},
      install_requires =['flask>=1.0.2','gensim>=3.7.2','inflect>=2.1.0','nltk>=3.3'],
      setup_requires   =['nltk'])
