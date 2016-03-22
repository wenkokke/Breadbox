from setuptools                 import setup, find_packages
from setuptools.command.install import install as _install


class Install(_install):
    def run(self):
        _install.do_egg_install(self)
        import nltk
        nltk.download('wordnet')
        nltk.download('cmudict')


setup(name='Breadbox',
      version          ='1.0',
      description      ='Implementation of "Breadbox" or "Plenty Questions".',
      author           ='Pepijn Kokke',
      author_email     ='pepijn.kokke@gmail.com',
      url              ='http://www.python.org/sigs/distutils-sig/',
      cmdclass         ={'install': Install},
      install_requires =['Flask>=0.10.1','future','names','enum','numpy'
                        ,'scipy','cython','sparsesvd','dissect','nltk'],
      setup_requires   =['nltk'])
