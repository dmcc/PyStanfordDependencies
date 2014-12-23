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

class Corpus(list):
    """Sequence of Sentence objects."""
    def as_conll(self):
        """Represent the entire corpus in CoNLL-X format."""
        return '\n'.join(sentence.as_conll() for sentence in self)
    @classmethod
    def from_conll(this_class, stream, token_filter=None):
        """stream is an iterable over strings. Returns a list of Sentence
        objects (essentially a list of Token objects). token_filter is
        an optional predicate applied to each Token. If False, we will
        not include the Token in the Sentence."""
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
                if token_filter and not token_filter(token):
                    continue
                current_sentence.append(token)
            else:
                flush()
        flush()
        return corpus
