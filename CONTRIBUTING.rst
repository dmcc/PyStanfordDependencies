Contributing to PyStanfordDependencies
======================================
We love pull requests from everyone. By participating in this project,
you agree to abide by the thoughtbot `code of
conduct <https://thoughtbot.com/open-source-code-of-conduct>`__.

Getting involved
----------------
If you're looking for ideas, see the list of known
`issues <https://github.com/dmcc/PyStanfordDependencies/issues>`__,
specifically those marked
"`help-wanted <https://github.com/dmcc/PyStanfordDependencies/issues?q=is%3Aopen+is%3Aissue+label%3A%22help+wanted%22>`__."

Submitting changes
------------------
-  Sign the `Contributor License
   Agreement <https://www.dropbox.com/s/woyyhxej4y0t2rw/cla-individual-PyStanfordDependencies.rtf?dl=1>`__.
   Email us if you have any questions about this.

-  Fork, then clone the repo::

       git clone git@github.com:your-username/PyStanfordDependencies.git

-  Make your changes (please include an update to ``CONTRIBUTORS.rst``)

-  Test your code's formatting with ``flake8 StanfordDependencies`` and
   output with ``nosetests`` (you will need to install ``flake8``,
   ``JPype1``, ``nose``, ``graphviz``, and ``asciitree`` packages via
   pip).  You'll need some implementation of Java 1.8 to run the tests.
   Changes should be tested with Python 2.7 and Python 3.4 (both will be
   tested with Travis CI (see below) if you don't want to create multiple
   environments). More information is available in the `release checklist
   <https://github.com/dmcc/PyStanfordDependencies/blob/master/CHECKLIST.txt>`__).
   If you add new code, please add appropriate
   testing code as well in ``tests/``. See `coveralls
   <https://coveralls.io/r/dmcc/PyStanfordDependencies?branch=master>`__
   for current test coverage. All new code should include at least some
   test that covers it.

-  Push to your fork and `submit a pull request
   <https://github.com/dmcc/PyStanfordDependencies/compare/>`__. `Travis
   CI <https://travis-ci.org/dmcc/PyStanfordDependencies/pull_requests>`__
   will `test
   <https://github.com/dmcc/PyStanfordDependencies/blob/master/.travis.yml>`__
   your changes on various Python versions.
