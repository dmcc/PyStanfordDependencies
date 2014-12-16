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

import jpype
from .StanfordDependencies import StanfordDependencies
from .Token import Token

class JPypeBackend(StanfordDependencies):
    """Faster backend than SubprocessBackend but requires you to install
    jpype ('pip install JPype1', not 'JPype'). May be less stable. There's
    no speed benefit of using convert_trees() over convert_tree() for this
    backend. In terms of output, should be identical to SubprocessBackend
    except that all string fields will be unicode. Additionally, has
    the option to run the lemmatizer (see convert_tree())."""
    def __init__(self, jar_filename=None, download_if_missing=False,
                 version=None, extra_jvm_args=None, start_jpype=True):
        """extra_jvm_args can be set to a list of strings which will
        be passed to your JVM.  If start_jpype is True, we will start
        a JVM via JPype if one hasn't been started already. The user is
        responsible for stopping the JVM (jpype.shutdownJVM()) when they
        are done converting. Once the JVM has been shutdown, you'll need
        to create a new JPypeBackend in order to convert after that."""
        StanfordDependencies.__init__(self, jar_filename, download_if_missing,
                                      version)
        if start_jpype and not jpype.isJVMStarted():
            jpype.startJVM(jpype.getDefaultJVMPath(), '-ea',
                           '-Djava.class.path=' + self.jar_filename,
                           *(extra_jvm_args or []))
        self.corenlp = jpype.JPackage('edu').stanford.nlp
        try:
            self.acceptFilter = self.corenlp.util.Filters.acceptFilter()
        except TypeError:
            # this appears to be caused by a mismatch between CoreNLP and JRE
            # versions since this method changed to return a Predicate.
            version = jpype.java.lang.System.getProperty("java.version")
            print "Your Java version:", version
            if version.startswith('1.7'):
                print "The last CoreNLP release for Java 1.7 was 3.4.1"
                print "Try using: StanfordDependencies.get_instance(backend='jpype', version='3.4.1')"
            print
            self.java_is_too_old()
        trees = self.corenlp.trees
        self.treeReader = trees.Trees.readTree
        self.grammaticalStructure = trees.EnglishGrammaticalStructure
        self.stemmer = self.corenlp.process.Morphology.stemStaticSynchronized
    def convert_tree(self, ptb_tree, representation='basic',
                     include_punct=True, include_erased=False,
                     add_lemmas=False):
        """Arguments are as in StanfordDependencies.convert_trees but with
        the addition of add_lemmas. If add_lemmas=True, we will run the
        Stanford CoreNLP lemmatizer and fill in the lemma field."""
        tree = self.treeReader(ptb_tree)
        if include_punct:
            egs = self.grammaticalStructure(tree, self.acceptFilter)
        else:
            egs = self.grammaticalStructure(tree)

        if representation == 'basic':
            deps = egs.typedDependencies()
        elif representation == 'collapsed':
            deps = egs.typedDependenciesCollapsed(True)
        elif representation == 'CCprocessed':
            deps = egs.typedDependenciesCCprocessed(True)
        elif representation == 'collapsedTree':
            deps = egs.typedDependenciesCollapsedTree()
        else:
            raise ValueError("Unknown representation: %r" % representation)

        head_and_deprel = {}
        for dep in deps:
            head_and_deprel[dep.dep().index()] = (dep.gov().index(),
                                                  dep.reln().toString())

        words = tree.taggedYield()
        tokens = []
        for index, word in enumerate(words, 1):
            if index in head_and_deprel:
                head, deprel = head_and_deprel[index]
            elif include_erased:
                head, deprel = 0, 'erased'
            else:
                continue
            form = word.value()
            tag = word.tag()
            if add_lemmas:
                lemma = self.stemmer(form, tag).word()
            else:
                lemma = None
            token = Token(index=index, form=form, lemma=lemma, cpos=tag,
                          pos=tag, feats=None, head=head, deprel=deprel,
                          phead=None, pdeprel=None)
            tokens.append(token)
        return tokens
