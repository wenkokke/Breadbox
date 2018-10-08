from setuptools                 import setup, find_packages
from setuptools.command.install import install as _install


class Install(_install):
    def run(self):
        _install.do_egg_install(self)
        import nltk
        nltk.download('wordnet')


setup(name='Breadbox',
      version          ='1.0',
      description      ='Implementation of "Breadbox" or "Plenty Questions".',
      author           ='Wen Kokke',
      author_email     ='wen.kokke@gmail.com',
      url              ='http://www.python.org/sigs/distutils-sig/',
      cmdclass         ={'install': Install},
      install_requires =['Flask>=0.10.1','future','names','enum','numpy','scipy'
                         ,'cython','sparsesvd','dissect','nltk','inflect'],
      setup_requires   =['nltk'])
