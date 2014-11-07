import jpype
from StanfordDependencies import StanfordDependencies, Token

class JPypeBackend(StanfordDependencies):
    def __init__(self, jar_filename=None, extra_jvm_args=None,
                 start_jpype=True):
        StanfordDependencies.__init__(self, jar_filename)
        if start_jpype:
            extra_jvm_args = extra_jvm_args or []
            jpype.startJVM(jpype.getDefaultJVMPath(), '-ea',
                           '-Djava.class.path=' + self.jar_filename,
                           *extra_jvm_args)
        self.corenlp = jpype.JPackage('edu').stanford.nlp
        self.acceptFilter = self.corenlp.util.Filters.acceptFilter()
        self.trees = self.corenlp.trees
        self.treeReader = self.trees.Trees.readTree
        self.grammaticalStructure = self.trees.EnglishGrammaticalStructure
        self.stemmer = self.corenlp.process.Morphology.stemStaticSynchronized
    def convert_tree(self, ptb_tree, representation='basic',
                     include_punc=True, lemmatize=True):
        tree = self.treeReader(ptb_tree)
        if include_punc:
            egs = self.grammaticalStructure(tree, self.acceptFilter)
        else:
            egs = self.grammaticalStructure(tree)

        if representation == 'basic':
            deps = egs.typedDependencies()
        elif representation == 'collapsed':
            deps = egs.typedDependenciesCollapsed()
        elif representation == 'CCprocessed':
            deps = egs.typedDependenciesCCprocessed()
        elif representation == 'tree':
            deps = egs.typedDependenciesCollapsedTree()
        else:
            raise ValueError("Unknown representation: %r" % representation)

        head_and_deprel = {}
        for dep in deps:
            head_and_deprel[dep.dep().index()] = (dep.gov().index(),
                                                  dep.reln().getShortName())

        words = tree.taggedYield()
        tokens = []
        for index, word in enumerate(words, 1):
            head, deprel = head_and_deprel[index]
            form = word.value()
            tag = word.tag()
            if lemmatize:
                lemma = self.stemmer(form, tag).word()
            else:
                lemma = None
            token = Token(index=index, form=form, cpos=tag, pos=tag,
                          head=head, deprel=deprel, lemma=lemma)
            tokens.append(token)
        return tokens

if __name__ == "__main__":
    sd = JPypeBackend()
    sd.download_if_missing()
    def print_sentences(sentences):
        for sentence in sentences:
            print '---'
            for token in sentence:
                print token
        print

    sent = sd.convert_tree('(S1 (NP (DT some) (NNS cows) (. .)))',
                           representation='CCprocessed')
    print_sentences([sent])
    jpype.shutdownJVM()
