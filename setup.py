from setuptools import setup

setup(name='Breadbox',
      version='1.0',
      description='A basic Flask app with static files',
      author='Pepijn Kokke',
      author_email='pepijnkokke@gmail.com',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=['Flask>=0.10.1'
                       ,'future'
                       ,'names'
                       ,'enum'
                       ,'numpy'
                       ,'scipy'
                       ,'cython'
                       ,'sparsesvd'
                       ,'dissect'
                       ,'nltk'])
