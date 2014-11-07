from abc import ABCMeta, abstractmethod

LATEST_VERSION = '3.5.0'
LATEST_JAR_FILENAME = 'stanford-corenlp-%s.jar' % LATEST_VERSION
# the maven version is smaller than the full CoreNLP distributions
LATEST_JAR_URL = 'http://search.maven.org/remotecontent?filepath=edu/stanford/nlp/stanford-corenlp/%s/%s' % (LATEST_VERSION, LATEST_JAR_FILENAME)
DEFAULT_INSTALL_DIR = '~/.local/share/pystanforddeps'

FIELD_NAMES = ('index', 'form', 'lemma', 'cpos', 'pos', 'feats', 'head',
               'deprel', 'phead', 'pdeprel')

class Token:
    """A CoNLL-X style dependency token. Fields include:
    - form (the word form)
    - pos (part of speech tag)
    - index (index of the token in the sentence)
    - head (index of the head of this token), and
    - deprel (the dependency relation between this token and its head)

    (there are other fields but they typically won't be populated here)"""
    def __init__(self, **fields):
        self.__dict__.update(fields)
    def __repr__(self):
        items = [(field, getattr(self, field, None)) for field in FIELD_NAMES]
        fields = ['%s=%r' % (k, v) for k, v in items if v is not None]
        return '%s(%s)' % (str(self.__class__).replace('__main__.', ''),
                           ', '.join(fields))

    @classmethod
    def from_string(this_class, text):
        fields = text.split('\t')
        fields[0] = int(fields[0]) # index
        fields[6] = int(fields[6]) # head index
        fields = [value if value != '_' else None for value in fields]
        return this_class(**dict(zip(FIELD_NAMES, fields)))

class StanfordDependencies:
    """Abstract base class for converting Penn Treebank trees to Stanford
    Dependencies.  To actually use this, you'll want to instantiate one
    of the backends.

    If you do not currently have the appropriate Java jar files, the
    download_if_missing() method will help you fetch them.

    The java_command flag is the path to a java binary.

    Subclasses should (at minimum) override the convert_tree method. They
    may also want to override convert_trees if they require batch
    operation."""
    __metaclass__ = ABCMeta
    def __init__(self, jar_filename=None):
        """jar_filename should be the path to a Java jar file with
        classfiles from Stanford CoreNLP or Stanford Parser."""
        if not jar_filename:
            jar_filename = self.get_and_setup_default_install_path()
        self.jar_filename = jar_filename

    def convert_trees(self, ptb_trees, representation='basic', **kwargs):
        """Convert a list of Penn Treebank formatted trees (ptb_trees)
        into Stanford Dependencies. The dependencies are represented
        as a list of sentences, where each sentence is itself a list of
        Token objects.

        Currently supported representations are 'basic', 'collapsed',
        'CCprocessed', and 'collapsedTree' which behave the same as they
        in the CoreNLP command line tools."""
        return [self.convert_tree(ptb_tree, representation=representation,
                                  **kwargs)
                for ptb_tree in ptb_trees]

    @abstractmethod
    def convert_tree(self, ptb_tree, representation='basic', **kwargs):
        """Converts a single Penn Treebank format tree to Stanford
        Dependencies. See convert_trees for more details."""

    def get_and_setup_default_install_path(self):
        """Determine the user-specific install path for the Stanford
        Dependencies jar if the jar_url is not specified and ensure that
        it is writable (that is, make sure the directory exists). Returns
        the full path for where the jar file should be installed."""
        import os
        import os.path

        install_dir = os.path.expanduser(DEFAULT_INSTALL_DIR)
        try:
            os.makedirs(install_dir)
        except OSError:
            pass
        jar_filename = os.path.join(install_dir, LATEST_JAR_FILENAME)
        return jar_filename
    def download_if_missing(self, jar_url=LATEST_JAR_URL, verbose=True):
        """Download jar_url into the jar_filename specified in the
        constructor. Will not overwrite jar_filename if it already
        exists."""
        import os.path
        if not os.path.exists(self.jar_filename):
            if verbose:
                print "Downloading %r -> %r" % (jar_url, self.jar_filename)
            import urllib
            urllib.urlretrieve(jar_url, filename=self.jar_filename)

    @staticmethod
    def get_instance(jar_filename=None, backend='jpype', **extra_args):
        if backend == 'jpype':
            try:
                from JPypeBackend import JPypeBackend
                return JPypeBackend(jar_filename, **extra_args)
            except ImportError:
                # fall back to subprocess backend which should work
                # more generally
                backend = 'subprocess'

        if backend == 'subprocess':
            from SubprocessBackend import SubprocessBackend
            return SubprocessBackend(jar_filename, **extra_args)
        else:
            raise ValueError("Unknown backend: %r" % backend)

if __name__ == "__main__":
    sd = StanfordDependencies.get_instance(backend='jpype')
    sd.download_if_missing()
    def print_sentences(sentences):
        for sentence in sentences:
            print '---'
            for token in sentence:
                print token
        print

    sents = sd.convert_trees(['(S1 (NP (DT a) (NN cow)))',
                              '(S1 (NP (DT some) (NNS cows)))',
                              '(S1 (NP (DT some) (JJ blue) (NN moose)))'],
                             representation='basic')
    print_sentences(sents)

    for representation in ('basic', 'collapsed', 'CCprocessed',
                           'collapsedTree'):
        print '%s representation' % representation
        print_sentences(sd.convert_trees(['(S1 (NP (NP (NP (DT A) (NN cat)) (CC and) (NP (DT a) (NN mouse))) (. .)))'], representation=representation))
