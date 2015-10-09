#!/usr/bin/env python
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

try:
    from setuptools import setup, Command
except ImportError:
    from distutils.core import setup, Command

class Test(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        self.run_command('flake8', 'StanfordDependencies')
        self.run_command('nosetests-2.7', '-dvx')
        self.run_command('nosetests-3.4', '-dvx')
    def run_command(self, *args):
        import subprocess
        print("Running %r" % ' '.join(args))
        exit_code = subprocess.call(args)
        print("Exit code: %s" % exit_code)
        if exit_code:
            raise SystemExit(exit_code)

setup(name='PyStanfordDependencies',
      version='0.3.0',
      description='Python interface for converting Penn Treebank trees to '
                  'Stanford Dependencies',
      long_description=open('README.rst').read(),
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
      packages=['StanfordDependencies'],
      extras_require={
          'JPype': ['JPype1'],
          'visualization': ['asciitree', 'graphviz'],
      },
      cmdclass={'test': Test})
