from setuptools import setup

setup(name='FlaskApp',
      version='1.0',
      description='A basic Flask app with static files',
      author='Ryan Jarvinen',
      author_email='ryanj@redhat.com',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=['Flask>=0.10.1'
                       ,'future'
                       ,'names'
                       ,'enum'
                       ,'numpy'
                       ,'scipy'
                       ,'cython'
                       ,'sparsesvd'
                       ,'dissect==0.1.0'
                       ,'nltk>=3.2'])
