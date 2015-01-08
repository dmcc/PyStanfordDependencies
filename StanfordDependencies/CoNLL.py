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

from collections import namedtuple
import re

# picks out (tag, word) from Penn Treebank-style trees
ptb_tags_and_words_re = re.compile(r'\(\s*([^\s()]+)\s+([^\s()]+)\s*\)')

# picks out (deprel, gov, govindex, dep, depindex) from Stanford
# Dependencies text (e.g., "nsubj(word-1, otherword-2)")
deps_re = re.compile(r'^\s*([^\s()]+)\(([^\s()]+)-(\d+),\s+'
                     r'([^\s()]+)-(\d+)\)\s*$',
                     re.M)

# CoNLL-X field names
FIELD_NAMES = ('index', 'form', 'lemma', 'cpos', 'pos', 'feats', 'head',
               'deprel', 'phead', 'pdeprel')

class Token(namedtuple('Token', FIELD_NAMES)):
    """CoNLL-X style dependency token. Fields include:
    - form (the word form)
    - lemma (the word's base form or lemma) -- empty for SubprocessBackend
    - pos (part of speech tag)
    - index (index of the token in the sentence)
    - head (index of the head of this token), and
    - deprel (the dependency relation between this token and its head)

    There are other fields but they typically won't be populated by
    StanfordDependencies.

    See http://ilk.uvt.nl/conll/#dataformat for a complete description."""
    def __repr__(self):
        """Represent this Token as Python code. Note that the resulting
        representation may not be a valid Python call since this skips
        fields with empty values."""
        # slightly different from the official tuple __repr__ in that
        # we skip any fields with None as their value
        items = [(field, getattr(self, field, None)) for field in FIELD_NAMES]
        fields = ['%s=%r' % (k, v) for k, v in items if v is not None]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(fields))
    def as_conll(self):
        """Represent this Token as a line in CoNLL-X format."""
        def get(field):
            value = getattr(self, field)
            if value is None:
                value = '_'
            elif field == 'feats':
                value = '|'.join(value)
            return str(value)
        return '\t'.join([get(field) for field in FIELD_NAMES])
    @classmethod
    def from_conll(this_class, text):
        """Construct a Token from a line in CoNLL-X format."""
        fields = text.split('\t')
        fields[0] = int(fields[0]) # index
        fields[6] = int(fields[6]) # head index
        if fields[5] != '_': # feats
            fields[5] = tuple(fields[5].split('|'))
        fields = [value if value != '_' else None for value in fields]
        return this_class(**dict(zip(FIELD_NAMES, fields)))

class Sentence(list):
    """Sequence of Token objects."""
    def as_conll(self):
        """Represent this Sentence in CoNLL-X format."""
        return '\n'.join(token.as_conll() for token in self)
    @classmethod
    def from_stanford_dependencies(this_class, stream, tree,
                                   include_erased=False, include_punct=True):
        """stream is an iterable over strings where each string is a
        line representing a Stanford Dependency as in the output of the
        command line Stanford Dependency tool:

            deprel(gov-index, dep-depindex)

        The corresponding Penn Treebank formatted tree must be provided
        as well. Returns a Sentence object (essentially a list of Token
        objects)."""
        sentence = this_class()
        covered_indices = set()
        tags_and_words = ptb_tags_and_words_re.findall(tree)
        for line in stream:
            if not line.strip():
                if sentence:
                    # empty line means the sentence is over
                    break
                else:
                    continue
            matches = deps_re.findall(line)
            assert len(matches) == 1
            deprel, gov_form, head, form, index = matches[0]
            index = int(index)
            tag, word = tags_and_words[index - 1]
            assert form == word
            covered_indices.add(index)

            if not include_punct and deprel == 'punct':
                continue
            token = Token(index, form, None, tag, tag, None, int(head),
                          deprel, None, None)
            sentence.append(token)

        if include_erased:
            # look through words in the tree to see if any of them
            # were erased
            for index, (tag, word) in enumerate(tags_and_words, 1):
                if index in covered_indices:
                    continue
                token = Token(index, word, None, tag, tag, None, 0,
                              'erased', None, None)
                sentence.append(token)

        sentence.sort()
        return sentence

class Corpus(list):
    """Sequence of Sentence objects."""
    def as_conll(self):
        """Represent the entire corpus in CoNLL-X format."""
        return '\n'.join(sentence.as_conll() for sentence in self)
    @classmethod
    def from_conll(this_class, stream):
        """stream is an iterable over strings where each string is a
        line in CoNLL-X format. Returns a Corpus object (essentially a
        list of Sentence objects)."""
        current_sentence = []
        corpus = this_class()
        def flush():
            if current_sentence:
                corpus.append(Sentence(current_sentence))
                del current_sentence[:]
        for line in stream:
            line = line.strip()
            if line:
                token = Token.from_conll(line)
                current_sentence.append(token)
            else:
                flush()
        flush()
        return corpus
    @classmethod
    def from_stanford_dependencies(this_class, stream, trees,
                                   include_erased=False, include_punct=True):
        """stream is an iterable over strings where each string is a
        line representing a Stanford Dependency as in the output of the
        command line Stanford Dependency tool:

            deprel(gov-index, dep-depindex)

        Sentences are separated by blank lines. A corresponding list of
        Penn Treebank formatted trees must be provided as well. Returns
        a Corpus object (list of Sentence objects which are a list of
        Token objects)."""
        stream = iter(stream)
        corpus = this_class()
        for tree in trees:
            sentence = Sentence.from_stanford_dependencies(stream,
                                                           tree,
                                                           include_erased,
                                                           include_punct)
            corpus.append(sentence)
        return corpus
