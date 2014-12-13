PySD
====

Python interface for converting Penn Treebank trees to `Stanford Dependencies <http://nlp.stanford.edu/software/stanford-dependencies.shtml>`_.

Example usage
-------------
Start by getting a StanfordDepenendencies instance with ``StanfordDependencies.get_instance``::

    >>> from StanfordDependencies import StanfordDependencies
    >>> sd = StanfordDependencies.get_instance(backend='subprocess')

This can take some options. ``backend`` can currently be ``subprocess``
or ``jpype`` (see below).  If you have an existing `Stanford CoreNLP
<http://nlp.stanford.edu/software/corenlp.shtml>`_ jar file, use
the ``jar_filename`` parameter to point to the full path of the jar
file. Otherwise, PySD will download a jar file for you and store it in
locally. You can request a specific version with the ``version`` flag,
e.g., ``version='3.4.1'``.  To convert trees, use the ``convert_tree``
or ``convert_trees`` method.  These return a sentence (list of ``Token``
objects) or a list of sentences (list of list of ``Token`` objects)
respectively::

    >>> sent = sd.convert_tree('(S1 (NP (DT some) (JJ blue) (NN moose)))')
    >>> for token in sent:
    ...     print token
    ... 
    StanfordDependencies.Token.Token(index=1, form='some', cpos='DT', pos='DT', head=3, deprel='det')
    StanfordDependencies.Token.Token(index=2, form='blue', cpos='JJ', pos='JJ', head=3, deprel='amod')
    StanfordDependencies.Token.Token(index=3, form='moose', cpos='NN', pos='NN', head=0, deprel='root')

This tells you that ``moose`` is the head of the sentence and is modified
by ``some`` (with a ``det`` = determiner relation) and ``blue`` (with an
``amod`` = adjective modifier relation).

Backends
--------
Currently PySD includes two backends:

- Subprocess (works anywhere with a ``java`` binary)
- JPype (requires `jpype1 <https://pypi.python.org/pypi/JPype1/0.5.7>`_
  from PyPI, faster than Subprocess, includes access to the Stanford
  CoreNLP lemmatizer)

More information
----------------
Licensed under `Apache 2.0 <http://www.apache.org/licenses/LICENSE-2.0>`_.

Written by David McClosky (`homepage <http://nlp.stanford.edu/~mcclosky/>`_, `code <http://github.com/dmcc>`_)

Bug reports and feature requests: `GitHub issue tracker <http://github.com/dmcc/PySD`_
