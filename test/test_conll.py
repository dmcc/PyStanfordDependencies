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

from StanfordDependencies.CoNLL import Corpus

def test_readwrite():
    # example from http://ilk.uvt.nl/conll/example.html
    sample_text = '''
1	Cathy	Cathy	N	N	eigen|ev|neut	2	su	_	_
2	zag	zie	V	V	trans|ovt|1of2of3|ev	0	ROOT	_	_
3	hen	hen	Pron	Pron	per|3|mv|datofacc	2	obj1	_	_
4	wild	wild	Adj	Adj	attr|stell|onverv	5	mod	_	_
5	zwaaien	zwaai	N	N	soort|mv|neut	2	vc	_	_
6	.	.	Punc	Punc	punt	5	punct	_	_
'''
    
    corpus = Corpus.from_conll(sample_text.splitlines())
    assert corpus.as_conll() == sample_text.strip()
