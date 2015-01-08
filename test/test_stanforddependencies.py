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

import unittest
from StanfordDependencies import (StanfordDependencies, get_instance,
                                  JavaRuntimeVersionError)
from StanfordDependencies.SubprocessBackend import SubprocessBackend
from StanfordDependencies.JPypeBackend import JPypeBackend

# these trees are produced with SD 3.4.1 since it allows us to test
# on older JREs
tree1 = '(S1 (NP (DT a) (NN cow)))'
tree1_out = '''
Token(index=1, form='a', cpos='DT', pos='DT', head=2, deprel='det')
Token(index=2, form='cow', cpos='NN', pos='NN', head=0, deprel='root')
'''.strip()

tree2 = '(S1 (NP (NP (NP (DT A) (NN cat)) (CC and) (NP (DT a) ' \
        '(NN mouse))) (. .)))'
tree2_out_basic = '''
Token(index=1, form='A', cpos='DT', pos='DT', head=2, deprel='det')
Token(index=2, form='cat', cpos='NN', pos='NN', head=0, deprel='root')
Token(index=3, form='and', cpos='CC', pos='CC', head=2, deprel='cc')
Token(index=4, form='a', cpos='DT', pos='DT', head=5, deprel='det')
Token(index=5, form='mouse', cpos='NN', pos='NN', head=2, deprel='conj')
Token(index=6, form='.', cpos='.', pos='.', head=2, deprel='punct')'''.strip()
tree2_out_collapsed = '''
Token(index=1, form='A', cpos='DT', pos='DT', head=2, deprel='det')
Token(index=2, form='cat', cpos='NN', pos='NN', head=0, deprel='root')
Token(index=4, form='a', cpos='DT', pos='DT', head=5, deprel='det')
Token(index=5, form='mouse', cpos='NN', pos='NN', head=2, deprel='conj_and')
Token(index=6, form='.', cpos='.', pos='.', head=2, deprel='punct')'''.strip()
tree2_out_CCprocessed = '''
Token(index=1, form='A', cpos='DT', pos='DT', head=2, deprel='det')
Token(index=2, form='cat', cpos='NN', pos='NN', head=0, deprel='root')
Token(index=4, form='a', cpos='DT', pos='DT', head=5, deprel='det')
Token(index=5, form='mouse', cpos='NN', pos='NN', head=2, deprel='conj_and')
Token(index=6, form='.', cpos='.', pos='.', head=2, deprel='punct')'''.strip()
tree2_out_collapsedTree = '''
Token(index=1, form='A', cpos='DT', pos='DT', head=2, deprel='det')
Token(index=2, form='cat', cpos='NN', pos='NN', head=0, deprel='root')
Token(index=4, form='a', cpos='DT', pos='DT', head=5, deprel='det')
Token(index=5, form='mouse', cpos='NN', pos='NN', head=2, deprel='conj_and')
Token(index=6, form='.', cpos='.', pos='.', head=2, deprel='punct')'''.strip()

tree3 = '(S1 (NP (DT some) (JJ blue) (NN moose)))'
tree3_out = '''
Token(index=1, form='some', cpos='DT', pos='DT', head=3, deprel='det')
Token(index=2, form='blue', cpos='JJ', pos='JJ', head=3, deprel='amod')
Token(index=3, form='moose', cpos='NN', pos='NN', head=0, deprel='root')
'''.strip()

tree4 = '(S1 (NP (NP (DT A) (NN burrito)) (PP (IN with) (NP (NP ' + \
        '(NNS beans)) (CONJP (CC but) (RB not)) (NP (NN chicken)))) (. .)))'
tree4_out_basic = '''
Token(index=1, form='A', cpos='DT', pos='DT', head=2, deprel='det')
Token(index=2, form='burrito', cpos='NN', pos='NN', head=0, deprel='root')
Token(index=3, form='with', cpos='IN', pos='IN', head=2, deprel='prep')
Token(index=4, form='beans', cpos='NNS', pos='NNS', head=3, deprel='pobj')
Token(index=5, form='but', cpos='CC', pos='CC', head=6, deprel='cc')
Token(index=6, form='not', cpos='RB', pos='RB', head=4, deprel='cc')
Token(index=7, form='chicken', cpos='NN', pos='NN', head=4, deprel='conj')
Token(index=8, form='.', cpos='.', pos='.', head=2, deprel='punct')
'''.strip()
tree4_out_collapsed = '''
Token(index=1, form='A', cpos='DT', pos='DT', head=2, deprel='det')
Token(index=2, form='burrito', cpos='NN', pos='NN', head=0, deprel='root')
Token(index=4, form='beans', cpos='NNS', pos='NNS', head=2, deprel='prep_with')
Token(index=7, form='chicken', cpos='NN', pos='NN', head=4, deprel='conj_negcc')
Token(index=8, form='.', cpos='.', pos='.', head=2, deprel='punct')
'''.strip()
tree4_out_CCprocessed = '''
Token(index=1, form='A', cpos='DT', pos='DT', head=2, deprel='det')
Token(index=2, form='burrito', cpos='NN', pos='NN', head=0, deprel='root')
Token(index=4, form='beans', cpos='NNS', pos='NNS', head=2, deprel='prep_with')
Token(index=7, form='chicken', cpos='NN', pos='NN', head=2, deprel='prep_with')
Token(index=7, form='chicken', cpos='NN', pos='NN', head=4, deprel='conj_negcc')
Token(index=8, form='.', cpos='.', pos='.', head=2, deprel='punct')
'''.strip()
tree4_out_collapsedTree = '''
Token(index=1, form='A', cpos='DT', pos='DT', head=2, deprel='det')
Token(index=2, form='burrito', cpos='NN', pos='NN', head=0, deprel='root')
Token(index=4, form='beans', cpos='NNS', pos='NNS', head=2, deprel='prep_with')
Token(index=7, form='chicken', cpos='NN', pos='NN', head=4, deprel='conj_negcc')
Token(index=8, form='.', cpos='.', pos='.', head=2, deprel='punct')
'''.strip()

tree5 = '''
(S1 (S (NP (NNP Ed))
     (VP (VBZ cooks)
      (CC and)
      (VBZ sells)
      (NP (NP (NNS burritos))
       (PP (IN with)
	(NP (NNS beans) (CONJP (CC but) (RB not)) (NN rice)))))
     (. .)))
'''.strip()
tree5_out_basic = '''
Token(index=1, form='Ed', cpos='NNP', pos='NNP', head=2, deprel='nsubj')
Token(index=2, form='cooks', cpos='VBZ', pos='VBZ', head=0, deprel='root')
Token(index=3, form='and', cpos='CC', pos='CC', head=2, deprel='cc')
Token(index=4, form='sells', cpos='VBZ', pos='VBZ', head=2, deprel='conj')
Token(index=5, form='burritos', cpos='NNS', pos='NNS', head=2, deprel='dobj')
Token(index=6, form='with', cpos='IN', pos='IN', head=5, deprel='prep')
Token(index=7, form='beans', cpos='NNS', pos='NNS', head=6, deprel='pobj')
Token(index=8, form='but', cpos='CC', pos='CC', head=9, deprel='cc')
Token(index=9, form='not', cpos='RB', pos='RB', head=7, deprel='cc')
Token(index=10, form='rice', cpos='NN', pos='NN', head=7, deprel='conj')
Token(index=11, form='.', cpos='.', pos='.', head=2, deprel='punct')
'''.strip()
tree5_out_collapsed = '''
Token(index=1, form='Ed', cpos='NNP', pos='NNP', head=2, deprel='nsubj')
Token(index=2, form='cooks', cpos='VBZ', pos='VBZ', head=0, deprel='root')
Token(index=4, form='sells', cpos='VBZ', pos='VBZ', head=2, deprel='conj_and')
Token(index=5, form='burritos', cpos='NNS', pos='NNS', head=2, deprel='dobj')
Token(index=7, form='beans', cpos='NNS', pos='NNS', head=5, deprel='prep_with')
Token(index=10, form='rice', cpos='NN', pos='NN', head=7, deprel='conj_negcc')
Token(index=11, form='.', cpos='.', pos='.', head=2, deprel='punct')
'''.strip()
tree5_out_CCprocessed = '''
Token(index=1, form='Ed', cpos='NNP', pos='NNP', head=2, deprel='nsubj')
Token(index=1, form='Ed', cpos='NNP', pos='NNP', head=4, deprel='nsubj')
Token(index=2, form='cooks', cpos='VBZ', pos='VBZ', head=0, deprel='root')
Token(index=4, form='sells', cpos='VBZ', pos='VBZ', head=2, deprel='conj_and')
Token(index=5, form='burritos', cpos='NNS', pos='NNS', head=2, deprel='dobj')
Token(index=7, form='beans', cpos='NNS', pos='NNS', head=5, deprel='prep_with')
Token(index=10, form='rice', cpos='NN', pos='NN', head=5, deprel='prep_with')
Token(index=10, form='rice', cpos='NN', pos='NN', head=7, deprel='conj_negcc')
Token(index=11, form='.', cpos='.', pos='.', head=2, deprel='punct')
'''.strip()
tree5_out_collapsedTree = '''
Token(index=1, form='Ed', cpos='NNP', pos='NNP', head=2, deprel='nsubj')
Token(index=2, form='cooks', cpos='VBZ', pos='VBZ', head=0, deprel='root')
Token(index=4, form='sells', cpos='VBZ', pos='VBZ', head=2, deprel='conj_and')
Token(index=5, form='burritos', cpos='NNS', pos='NNS', head=2, deprel='dobj')
Token(index=7, form='beans', cpos='NNS', pos='NNS', head=5, deprel='prep_with')
Token(index=10, form='rice', cpos='NN', pos='NN', head=7, deprel='conj_negcc')
Token(index=11, form='.', cpos='.', pos='.', head=2, deprel='punct')
'''.strip()
tree5_out_collapsedTree_no_punc = '''
Token(index=1, form='Ed', cpos='NNP', pos='NNP', head=2, deprel='nsubj')
Token(index=2, form='cooks', cpos='VBZ', pos='VBZ', head=0, deprel='root')
Token(index=4, form='sells', cpos='VBZ', pos='VBZ', head=2, deprel='conj_and')
Token(index=5, form='burritos', cpos='NNS', pos='NNS', head=2, deprel='dobj')
Token(index=7, form='beans', cpos='NNS', pos='NNS', head=5, deprel='prep_with')
Token(index=10, form='rice', cpos='NN', pos='NN', head=7, deprel='conj_negcc')
'''.strip()
tree5_out_collapsedTree_erased = '''
Token(index=1, form='Ed', cpos='NNP', pos='NNP', head=2, deprel='nsubj')
Token(index=2, form='cooks', cpos='VBZ', pos='VBZ', head=0, deprel='root')
Token(index=3, form='and', cpos='CC', pos='CC', head=0, deprel='erased')
Token(index=4, form='sells', cpos='VBZ', pos='VBZ', head=2, deprel='conj_and')
Token(index=5, form='burritos', cpos='NNS', pos='NNS', head=2, deprel='dobj')
Token(index=6, form='with', cpos='IN', pos='IN', head=0, deprel='erased')
Token(index=7, form='beans', cpos='NNS', pos='NNS', head=5, deprel='prep_with')
Token(index=8, form='but', cpos='CC', pos='CC', head=0, deprel='erased')
Token(index=9, form='not', cpos='RB', pos='RB', head=0, deprel='erased')
Token(index=10, form='rice', cpos='NN', pos='NN', head=7, deprel='conj_negcc')
Token(index=11, form='.', cpos='.', pos='.', head=2, deprel='punct')
'''.strip()
tree5_out_collapsedTree_erased_no_punct = '''
Token(index=1, form='Ed', cpos='NNP', pos='NNP', head=2, deprel='nsubj')
Token(index=2, form='cooks', cpos='VBZ', pos='VBZ', head=0, deprel='root')
Token(index=3, form='and', cpos='CC', pos='CC', head=0, deprel='erased')
Token(index=4, form='sells', cpos='VBZ', pos='VBZ', head=2, deprel='conj_and')
Token(index=5, form='burritos', cpos='NNS', pos='NNS', head=2, deprel='dobj')
Token(index=6, form='with', cpos='IN', pos='IN', head=0, deprel='erased')
Token(index=7, form='beans', cpos='NNS', pos='NNS', head=5, deprel='prep_with')
Token(index=8, form='but', cpos='CC', pos='CC', head=0, deprel='erased')
Token(index=9, form='not', cpos='RB', pos='RB', head=0, deprel='erased')
Token(index=10, form='rice', cpos='NN', pos='NN', head=7, deprel='conj_negcc')
'''.strip()
tree5_out_basic_lemmas = '''
Token(index=1, form='Ed', lemma='Ed', cpos='NNP', pos='NNP', head=2, deprel='nsubj')
Token(index=2, form='cooks', lemma='cook', cpos='VBZ', pos='VBZ', head=0, deprel='root')
Token(index=3, form='and', lemma='and', cpos='CC', pos='CC', head=2, deprel='cc')
Token(index=4, form='sells', lemma='sell', cpos='VBZ', pos='VBZ', head=2, deprel='conj')
Token(index=5, form='burritos', lemma='burrito', cpos='NNS', pos='NNS', head=2, deprel='dobj')
Token(index=6, form='with', lemma='with', cpos='IN', pos='IN', head=5, deprel='prep')
Token(index=7, form='beans', lemma='bean', cpos='NNS', pos='NNS', head=6, deprel='pobj')
Token(index=8, form='but', lemma='but', cpos='CC', pos='CC', head=9, deprel='cc')
Token(index=9, form='not', lemma='not', cpos='RB', pos='RB', head=7, deprel='cc')
Token(index=10, form='rice', lemma='rice', cpos='NN', pos='NN', head=7, deprel='conj')
Token(index=11, form='.', lemma='.', cpos='.', pos='.', head=2, deprel='punct')
'''.strip()

basic_tests = ((tree1, tree1_out), (tree2, tree2_out_basic), (tree3, tree3_out),
               (tree4, tree4_out_basic), (tree5, tree5_out_basic))
basic_tests = [(tree5, tree5_out_basic)]
repr_tests2 = dict(basic=tree2_out_basic, collapsed=tree2_out_collapsed,
                   CCprocessed=tree2_out_CCprocessed,
                   collapsedTree=tree2_out_collapsedTree)
repr_tests4 = dict(basic=tree4_out_basic, collapsed=tree4_out_collapsed,
                   CCprocessed=tree4_out_CCprocessed,
                   collapsedTree=tree4_out_collapsedTree)
repr_tests5 = dict(basic=tree5_out_basic, collapsed=tree5_out_collapsed,
                   CCprocessed=tree5_out_CCprocessed,
                   collapsedTree=tree5_out_collapsedTree)

def test_subprocess_backend_creation():
    sd = StanfordDependencies.get_instance(backend='subprocess',
                                           version='3.4.1',
                                           download_if_missing=True)
    assert isinstance(sd, SubprocessBackend)

def test_subprocess_backend_creation_shortcut():
    sd = get_instance(backend='subprocess', version='3.4.1',
                      download_if_missing=True)
    assert isinstance(sd, SubprocessBackend)

def test_subprocess_backend_creation_newest_version():
    sd = get_instance(backend='subprocess', version=None,
                      download_if_missing=True)
    assert isinstance(sd, SubprocessBackend)

def test_jpype_backend_creation():
    sd = StanfordDependencies.get_instance(backend='jpype',
                                           version='3.4.1',
                                           download_if_missing=True)
    assert isinstance(sd, JPypeBackend), \
           "Fell back to another backend due to a JPype error"

def stringify_sentence(tokens):
    from StanfordDependencies import CoNLL
    # this doesn't work in general, but for current tests we want all
    # the string fields to be strings, not unicode
    new_tokens = []
    for token in tokens:
        new_fields = []
        for field in CoNLL.FIELD_NAMES:
            value = getattr(token, field)
            if isinstance(value, basestring):
                value = str(value)
            new_fields.append(value)
        new_tokens.append(CoNLL.Token(*new_fields))
    return '\n'.join(repr(token) for token in new_tokens)

class DefaultBackendTest(unittest.TestCase):
    backend = None
    version = '3.4.1'
    def setUp(self):
        kwargs = dict(version=self.version, download_if_missing=True)
        if self.backend is not None:
            kwargs['backend'] = self.backend
        self.sd = StanfordDependencies.get_instance(**kwargs)
    def test_basic_single(self):
        for tree, expected in basic_tests:
            self.assertConverts(tree, expected)
    def test_basic_multiple(self):
        trees, expected_outputs = zip(*basic_tests)
        sentences = self.sd.convert_trees(trees)
        for tokens, expected in zip(sentences, expected_outputs):
            self.assertTokensMatch(tokens, expected)
    def test_reprs(self):
        for representation, expected in sorted(repr_tests2.items()):
            self.assertConverts(tree2, expected, representation=representation)
        for representation, expected in sorted(repr_tests4.items()):
            self.assertConverts(tree4, expected, representation=representation)
        for representation, expected in sorted(repr_tests5.items()):
            self.assertConverts(tree5, expected, representation=representation)
    def test_punct_and_erased(self):
        self.assertConverts(tree5, tree5_out_collapsedTree_no_punc,
                            representation='collapsedTree',
                            include_punct=False, include_erased=False)
        self.assertConverts(tree5, tree5_out_collapsedTree_erased_no_punct,
                            representation='collapsedTree',
                            include_punct=False, include_erased=True)
        self.assertConverts(tree5, tree5_out_collapsedTree,
                            representation='collapsedTree',
                            include_punct=True, include_erased=False)
        self.assertConverts(tree5, tree5_out_collapsedTree_erased,
                            representation='collapsedTree',
                            include_punct=True, include_erased=True)
    def test_bogus_representation(self):
        self.assertRaises(ValueError, self.sd.convert_tree, tree1,
                          representation='bogus')
    def test_bogus_backend_creation(self):
        self.assertRaises(ValueError, StanfordDependencies.get_instance,
                          backend='bogus')
    def test_bogus_version(self):
        self.assertRaises(ValueError, StanfordDependencies.get_instance,
                          version='bogus')
        self.assertRaises(ValueError, StanfordDependencies.get_instance,
                          version='0')
        self.assertRaises(TypeError, StanfordDependencies.get_instance,
                          version=0)
    def test_insufficient_jar_info(self):
        self.assertRaises(ValueError, StanfordDependencies.get_instance,
                          backend=self.backend, jar_filename=None,
                          download_if_missing=False, version=None)
    def test_get_jar_url(self):
        assert self.sd.get_jar_url(version='3.5.0') == \
            "http://search.maven.org/remotecontent?filepath=edu/" \
            "stanford/nlp/stanford-corenlp/3.5.0/stanford-corenlp-3.5.0.jar"
        # unclear what it should be since it can change but it should
        # at least be a true value
        assert self.sd.get_jar_url()
    def test_get_jar_url_bad_version(self):
        self.assertRaises(TypeError, self.sd.get_jar_url, 0)
        self.assertRaises(TypeError, self.sd.get_jar_url, -1)
        self.assertRaises(TypeError, self.sd.get_jar_url, 10)
        self.assertRaises(TypeError, self.sd.get_jar_url, (3, 5, 0))

    def assertConverts(self, tree, expected, **conversion_options):
        print 'tree:'
        print tree
        print 'conversion_options:'
        print conversion_options
        tokens = self.sd.convert_tree(tree, **conversion_options)
        self.assertTokensMatch(tokens, expected)
    def assertTokensMatch(self, tokens, expected_stringification):
        stringified = stringify_sentence(tokens)
        print 'actual stringified:'
        print stringified
        print 'expected stringified:'
        print expected_stringification
        print 'matches:', stringified == expected_stringification
        assert stringified == expected_stringification
        print

class SubprocessBackendTest(DefaultBackendTest):
    backend = 'subprocess'
    version = '3.4.1'

    def test_raise_on_bad_exitcode(self):
        self.assertRaises(ValueError,
                          self.sd._raise_on_bad_exitcode, 100, '')
        self.assertRaises(ValueError,
                          self.sd._raise_on_bad_exitcode, 1, '')
        self.assertRaises(ValueError,
                          self.sd._raise_on_bad_exitcode, -1, '')
        self.assertRaises(JavaRuntimeVersionError,
                          self.sd._raise_on_bad_exitcode, 1,
                          'Unsupported major.minor version')
        self.assertRaises(JavaRuntimeVersionError,
                          self.sd._raise_on_bad_exitcode, -7,
                          'Unsupported major.minor version',
                          debug=True)
        self.sd._raise_on_bad_exitcode(0, '') # shouldn't raise anything

    def test_convert_debug(self):
        self.assertConverts(tree1, tree1_out, debug=True)

class JPypeBackendTest(DefaultBackendTest):
    backend = 'jpype'
    version = '3.4.1'

    def test_add_lemmas(self):
        self.assertConverts(tree5, tree5_out_basic_lemmas, add_lemmas=True)
    def test_report_version_error(self):
        self.assertRaises(JavaRuntimeVersionError,
                          self.sd._report_version_error, '1.6')
