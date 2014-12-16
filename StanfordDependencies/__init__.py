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

"""
PyStanfordDependencies
======================

Python interface for converting `Penn Treebank
<http://www.cis.upenn.edu/~treebank/>`_ trees to `Stanford Dependencies
<http://nlp.stanford.edu/software/stanford-dependencies.shtml>`_.

Example usage
-------------
Start by getting a ``StanfordDependencies`` instance with
``StanfordDependencies.get_instance()``::

    >>> import StanfordDependencies
    >>> sd = StanfordDependencies.get_instance(backend='subprocess')

``get_instance()`` takes several options. ``backend`` can currently
be ``subprocess`` or ``jpype`` (see below).  If you have an existing
`Stanford CoreNLP <http://nlp.stanford.edu/software/corenlp.shtml>`_ or
`Stanford Parser <http://nlp.stanford.edu/software/lex-parser.shtml>`_
jar file, use the ``jar_filename`` parameter to point to the full path of
the jar file. Otherwise, PyStanfordDependencies will download a jar file
for you and store it in locally (``~/.local/share/pystanforddeps``). You
can request a specific version with the ``version`` flag, e.g.,
``version='3.4.1'``.  To convert trees, use the ``convert_tree()`` or
``convert_trees()`` method.  These return a sentence (list of ``Token``
objects) or a list of sentences (list of list of ``Token`` objects)
respectively::

    >>> sent = sd.convert_tree('(S1 (NP (DT some) (JJ blue) (NN moose)))')
    >>> for token in sent:
    ...     print token
    ...
    Token(index=1, form='some', cpos='DT', pos='DT', head=3, deprel='det')
    Token(index=2, form='blue', cpos='JJ', pos='JJ', head=3, deprel='amod')
    Token(index=3, form='moose', cpos='NN', pos='NN', head=0, deprel='root')

This tells you that ``moose`` is the head of the sentence and is
modified by ``some`` (with a ``det`` = determiner relation) and ``blue``
(with an ``amod`` = adjective modifier relation). Fields on ``Token``
objects are readable as attributes. See docs for addtional options in
``convert_tree()`` and ``convert_trees()``.

Backends
--------
Currently PyStanfordDependencies includes two backends:

- ``subprocess`` (works anywhere with a ``java`` binary, slow so
  conversions with ``convert_trees()`` are recommended)
- ``jpype`` (requires `jpype1 <https://pypi.python.org/pypi/JPype1>`_,
  faster than Subprocess, includes access to the Stanford CoreNLP
  lemmatizer)

By default, it will attempt to use the ``jpype`` backend and fallback to
``subprocess`` with a warning.

More information
----------------
Licensed under `Apache 2.0 <http://www.apache.org/licenses/LICENSE-2.0>`_.

Written by David McClosky (`homepage <http://nlp.stanford.edu/~mcclosky/>`_, `code <http://github.com/dmcc>`_)

Bug reports and feature requests: `GitHub issue tracker <http://github.com/dmcc/PyStanfordDependencies/issues>`_
"""

from .StanfordDependencies import StanfordDependencies, get_instance
from .Token import Token

__authors__ = 'David McClosky'
__license__ = 'Apache 2.0'
__version__ = '0.1.1'
__email__ = 'notsoweird+pystanforddependencies@gmail.com'
