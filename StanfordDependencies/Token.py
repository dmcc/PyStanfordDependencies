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

# CoNLL-X field names
FIELD_NAMES = ('index', 'form', 'lemma', 'cpos', 'pos', 'feats', 'head',
               'deprel', 'phead', 'pdeprel')

class Token:
    """A CoNLL-X style dependency token. Fields include:
    - form (the word form)
    - lemma (the word's base form or lemma) -- empty for SubprocessBackend
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
