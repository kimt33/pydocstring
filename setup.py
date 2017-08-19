from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='pydocstyle',
      version='0.0.1',
      description='Collection of tools for manipulating Python docstrings.',
      long_description=long_description,
      url='https://github.com/kimt33/pydocstring',
      author='Taewon D. Kim',
      author_email='david.kim.91@gmail.com',
      license='MIT',
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: People that write docstrings',
                   'Topic :: Software Development :: Docstring',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3'],
      keywords='docstring',
      packages=['pydocstring'],
      install_requires=[],
      extras_require={},
      package_data={},
      data_files=[],
      entry_points={'console_scripts': []},
      )
