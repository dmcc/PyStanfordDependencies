#!/usr/bin/env python

from distutils.core import setup

setup(name='PyStanfordDependencies',
      version='0.1.6',
      description='Python interface for converting Penn Treebank trees to '
                  'Stanford Dependencies',
      long_description=file('README.rst').read(),
      author='David McClosky',
      author_email='notsoweird+pystanforddependencies@gmail.com',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: Apache Software License',
          'Natural Language :: English',
          'Operating System :: POSIX',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
      ],
      url='http://github.com/dmcc/PyStanfordDependencies',
      license='Apache 2.0',
      platforms=['POSIX'],
      packages=['StanfordDependencies'])
