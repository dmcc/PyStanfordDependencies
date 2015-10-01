#!/usr/bin/env python

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
      version='0.2.0',
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
      cmdclass={'test': Test})
