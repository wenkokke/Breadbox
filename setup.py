from setuptools import setup, find_packages
from setuptools.command.install import install as _install

class Install(_install):
    def run(self):
        _install.do_egg_install(self)
        import nltk
        nltk.download("wordnet")

setup(name='Breadbox',
      version          = '2.0',
      description      = 'Implementation of "Breadbox" or "Plenty Questions".',
      author           = 'Wen Kokke',
      author_email     = 'wen.kokke@gmail.com',
      url              = 'http://www.python.org/sigs/distutils-sig/',
      cmdclass         = {'install': Install},
      install_requires = ['flask>=1.0.2','gensim>=3.7.2','inflect>=2.1.0','nltk>=3.3'],
      setup_requires   = ['nltk'],)
