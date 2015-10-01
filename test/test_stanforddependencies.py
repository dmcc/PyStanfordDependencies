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

from __future__ import print_function
import unittest
from StanfordDependencies import (StanfordDependencies, get_instance,
                                  JavaRuntimeVersionError)
from StanfordDependencies.SubprocessBackend import SubprocessBackend
from StanfordDependencies.JPypeBackend import JPypeBackend
from StanfordDependencies.CoNLL import Corpus, Sentence, Token
from .data import trees_sd, trees_ud

def stringify_sentence(tokens):
    """Helper utility which standardizes stringification for testing."""
    from StanfordDependencies import CoNLL
    new_tokens = []

    try:
        string_type = basestring
    except NameError:
        string_type = str

    for token in tokens:
        new_fields = []
        for field in CoNLL.FIELD_NAMES_PLUS:
            value = getattr(token, field)
            if isinstance(value, string_type):
                value = str(value)
            new_fields.append(value)
        new_tokens.append(CoNLL.Token(*new_fields))
    return '\n'.join(repr(token) for token in new_tokens)

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
                                           version='3.5.2',
                                           download_if_missing=True)
    assert isinstance(sd, JPypeBackend), \
           "Fell back to another backend due to a JPype error"

class DefaultBackendTest(unittest.TestCase):
    backend = None
    version = '3.5.2'
    universal = False

    def setUp(self):
        if self.universal:
            self.trees = trees_ud
        else:
            self.trees = trees_sd

        kwargs = dict(version=self.version, download_if_missing=True)
        if self.backend is not None:
            kwargs['backend'] = self.backend
        self.sd = StanfordDependencies.get_instance(**kwargs)
    def test_basic_single(self):
        for tree, expected in self.trees.get_basic_test_trees():
            self.assertConverts(tree, expected)
    def test_basic_multiple(self):
        trees, expected_outputs = zip(*self.trees.get_basic_test_trees())
        sentences = self.sd.convert_trees(trees, universal=self.universal)
        assert len(sentences) == len(expected_outputs)
        assert isinstance(sentences, Corpus)
        assert isinstance(sentences[0], Sentence)
        assert isinstance(sentences[0][0], Token)
        for tree, tokens, expected in zip(trees, sentences, expected_outputs):
            self.assertTokensMatch(tree, tokens, expected)
    def test_reprs(self):
        for representation, expected in self.trees.get_repr_test_tree2():
            self.assertConverts(self.trees.tree2, expected,
                                representation=representation)
        for representation, expected in self.trees.get_repr_test_tree4():
            self.assertConverts(self.trees.tree4, expected,
                                representation=representation)
        for representation, expected in self.trees.get_repr_test_tree5():
            self.assertConverts(self.trees.tree5, expected,
                                representation=representation)
        for representation, expected in self.trees.get_repr_test_tree8():
            self.assertConverts(self.trees.tree8, expected,
                                representation=representation)
    def test_punct_and_erased(self):
        self.assertConverts(self.trees.tree5,
                            self.trees.tree5_out_collapsedTree_no_punct,
                            representation='collapsedTree',
                            include_punct=False, include_erased=False)
        self.assertConverts(self.trees.tree5,
                            self.trees.tree5_out_collapsedTree_erased_no_punct,
                            representation='collapsedTree',
                            include_punct=False, include_erased=True)
        self.assertConverts(self.trees.tree5,
                            self.trees.tree5_out_collapsedTree,
                            representation='collapsedTree',
                            include_punct=True, include_erased=False)
        self.assertConverts(self.trees.tree5,
                            self.trees.tree5_out_collapsedTree_erased,
                            representation='collapsedTree',
                            include_punct=True, include_erased=True)
    def test_bogus_input_type(self):
        self.assertRaises(TypeError, self.sd.convert_tree, ['bogus'])
        self.assertRaises(TypeError, self.sd.convert_tree, [-7, 7, -4])
        self.assertRaises(TypeError, self.sd.convert_tree, 3)
        self.assertRaises(TypeError, self.sd.convert_tree, {})
        self.assertRaises(TypeError, self.sd.convert_tree, open)
        self.assertRaises(TypeError, self.sd.convert_tree, str)
        self.assertRaises(TypeError, self.sd.convert_trees, 3)
        self.assertRaises(TypeError, self.sd.convert_trees, {444: 555})
        self.assertRaises(TypeError, self.sd.convert_trees, [1, 2, 3])
    def test_bogus_input_value(self):
        self.assertRaises(ValueError, self.sd.convert_tree, '(S')
        self.assertRaises(ValueError, self.sd.convert_tree, '')
        self.assertRaises(ValueError, self.sd.convert_tree, ' ')
        self.assertRaises(ValueError, self.sd.convert_tree, '\n')
        self.assertRaises(ValueError, self.sd.convert_tree, '"')
        self.assertRaises(ValueError, self.sd.convert_tree, '((Hi there)')
        self.assertRaises(ValueError, self.sd.convert_tree, 'bogus')
        self.assertRaises(ValueError, self.sd.convert_tree, 'bogus)')
        self.assertRaises(ValueError, self.sd.convert_tree, 'bogus))')
    def test_bogus_representation(self):
        self.assertRaises(ValueError, self.sd.convert_tree, self.trees.tree1,
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

    #
    # helper functions
    #
    def assertConverts(self, tree, expected, **conversion_options):
        conversion_options.setdefault('universal', self.universal)
        print('conversion_options:')
        print(conversion_options)
        tokens = self.sd.convert_tree(tree, **conversion_options)
        self.assertTokensMatch(tree, tokens, expected)
    def assertTokensMatch(self, tree, tokens, expected_stringification):
        print('tree:')
        print(tree)
        stringified = stringify_sentence(tokens)
        print('actual stringified:')
        print(stringified)
        print('expected stringified:')
        print(expected_stringification)
        print('matches:', stringified == expected_stringification)
        assert stringified == expected_stringification
        print()

class SubprocessBackendTest(DefaultBackendTest):
    backend = 'subprocess'

    def test_raise_on_bad_exitcode(self):
        self.assertRaises(ValueError,
                          self.sd._raise_on_bad_exit_or_output, 100, '')
        self.assertRaises(ValueError,
                          self.sd._raise_on_bad_exit_or_output, 1, '')
        self.assertRaises(ValueError,
                          self.sd._raise_on_bad_exit_or_output, -1, '')
        self.assertRaises(JavaRuntimeVersionError,
                          self.sd._raise_on_bad_exit_or_output, 1,
                          'Unsupported major.minor version')
        self.assertRaises(JavaRuntimeVersionError,
                          self.sd._raise_on_bad_exit_or_output, -7,
                          'Unsupported major.minor version')
        self.assertRaises(JavaRuntimeVersionError,
                          self.sd._raise_on_bad_exit_or_output, 1,
                          'JVMCFRE003 bad major version')
        self.assertRaises(JavaRuntimeVersionError,
                          self.sd._raise_on_bad_exit_or_output, -7,
                          'JVMCFRE003 bad major version')
        self.sd._raise_on_bad_exit_or_output(0, '') # shouldn't raise anything

    def test_convert_debug(self):
        self.assertConverts(self.trees.tree1, self.trees.tree1_out, debug=True)

class UDSubprocessBackendTest(SubprocessBackendTest):
    universal = True

class JPypeBackendTest(DefaultBackendTest):
    backend = 'jpype'

    def test_add_lemmas(self):
        self.assertConverts(self.trees.tree5,
                            self.trees.tree5_out_basic_lemmas,
                            add_lemmas=True)
    def test_report_version_error(self):
        self.assertRaises(JavaRuntimeVersionError,
                          self.sd._report_version_error, '1.6')

class UDJPypeBackendTest(JPypeBackendTest):
    universal = True
