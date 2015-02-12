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

import sys
from StanfordDependencies.CoNLL import Corpus, Sentence
from test_stanforddependencies import (tree4, tree4_out_CCprocessed,
                                       tree5, tree5_out_CCprocessed,
                                       tree5_out_collapsedTree_no_punc,
                                       stringify_sentence)

older_than_py27 = sys.version_info[:2] < (2, 7)

# example from http://ilk.uvt.nl/conll/example.html
conll_example = '''
1	Cathy	Cathy	N	N	eigen|ev|neut	2	su	_	_
2	zag	zie	V	V	trans|ovt|1of2of3|ev	0	ROOT	_	_
3	hen	hen	Pron	Pron	per|3|mv|datofacc	2	obj1	_	_
4	wild	wild	Adj	Adj	attr|stell|onverv	5	mod	_	_
5	zwaaien	zwaai	N	N	soort|mv|neut	2	vc	_	_
6	.	.	Punc	Punc	punt	5	punct	_	_
'''

def test_conll_readwrite_sentence():
    sentence = Sentence.from_conll(conll_example.splitlines())
    assert sentence.as_conll() == conll_example.strip()

def test_conll_readwrite_corpus():
    corpus = Corpus.from_conll(conll_example.splitlines())
    assert corpus.as_conll() == conll_example.strip()

def test_conll_as_asciitree():
    asciitree_out = '''
 zag [ROOT]
  +-- Cathy [su]
  +-- hen [obj1]
  +-- zwaaien [vc]
     +-- wild [mod]
     +-- . [punct]'''

    sentence = Sentence.from_conll(conll_example.splitlines())
    assert sentence.as_asciitree().strip() == asciitree_out.strip()

def test_conll_as_asciitree_custom():
    asciitree_out = '''
ROOT:zag:V
  +--su:Cathy:N
  +--obj1:hen:Pron
  +--vc:zwaaien:N
     +--mod:wild:Adj
     +--punct:.:Punc'''

    def str_func(token):
        return '%s:%s:%s' % (token.deprel, token.form, token.cpos)
    sentence = Sentence.from_conll(conll_example.splitlines())
    assert sentence.as_asciitree(str_func=str_func).strip() == \
           asciitree_out.strip()

def test_conll_as_asciitree_nontree():
    sample_deps = '''
det(burrito-2, A-1)
root(ROOT-0, burrito-2)
prep_with(burrito-2, beans-4)
prep_with(burrito-2, chicken-7)
conj_negcc(beans-4, chicken-7)
punct(burrito-2, .-8)
    '''.strip().splitlines()
    sentence = Sentence.from_stanford_dependencies(sample_deps, tree4)
    assert len(sentence) == 6
    assert sentence.as_asciitree().strip() == '''
 burrito [root]
  +-- A [det]
  +-- beans [prep_with]
  |  +-- chicken [conj_negcc]
  +-- chicken [prep_with]
  +-- . [punct]
'''.strip()

def test_conll_as_asciitree_nontree_erased():
    sample_deps = '''
det(burrito-2, A-1)
root(ROOT-0, burrito-2)
prep_with(burrito-2, beans-4)
prep_with(burrito-2, chicken-7)
conj_negcc(beans-4, chicken-7)
punct(burrito-2, .-8)
    '''.strip().splitlines()
    sentence = Sentence.from_stanford_dependencies(sample_deps, tree4,
                                                   include_erased=True)
    assert len(sentence) == 9
    assert sentence.as_asciitree().strip() == '''
 ROOT [ROOT-DEPREL]
  +-- burrito [root]
  |  +-- A [det]
  |  +-- beans [prep_with]
  |  |  +-- chicken [conj_negcc]
  |  +-- chicken [prep_with]
  |  +-- . [punct]
  +-- with [erased]
  +-- but [erased]
  +-- not [erased]
'''.strip()

def test_conll_as_dotgraph_nontree():
    if older_than_py27: # this feature disabled in older Pythons
        return
    sample_deps = '''
det(burrito-2, A-1)
root(ROOT-0, burrito-2)
prep_with(burrito-2, beans-4)
prep_with(burrito-2, chicken-7)
conj_negcc(beans-4, chicken-7)
punct(burrito-2, .-8)
    '''.strip().splitlines()
    sentence = Sentence.from_stanford_dependencies(sample_deps, tree4)
    assert len(sentence) == 6
    assert sentence.as_dotgraph().source == '''
digraph {
	0 [label=root]
	1 [label=A]
		2 -> 1 [label=det]
	2 [label=burrito]
		0 -> 2 [label=root]
	4 [label=beans]
		2 -> 4 [label=prep_with]
	7 [label=chicken]
		2 -> 7 [label=prep_with]
		4 -> 7 [label=conj_negcc]
	8 [label="."]
		2 -> 8 [label=punct]
}
'''.strip()

def test_conll_as_dotgraph_custom_digraph_and_idprefix():
    if older_than_py27: # this feature disabled in older Pythons
        return
    formatted_dotgraph = '''
digraph test {
	x0 [label=root]
	x1 [label=Cathy]
		x2 -> x1 [label=su]
	x2 [label=zag]
		x0 -> x2 [label=ROOT]
	x3 [label=hen]
		x2 -> x3 [label=obj1]
	x4 [label=wild]
		x5 -> x4 [label=mod]
	x5 [label=zwaaien]
		x2 -> x5 [label=vc]
	x6 [label="."]
		x5 -> x6 [label=punct]
}'''.strip()

    sentence = Sentence.from_conll(conll_example.splitlines())
    dotgraph = sentence.as_dotgraph(id_prefix='x',
                                    digraph_kwargs={'name': 'test'})

def test_conll_as_dotgraph_custom_nodeformat():
    if older_than_py27: # this feature disabled in older Pythons
        return
    formatted_dotgraph = '''
digraph {
	0 [label=root color=red]
	1 [label=Cathy color=green]
		2 -> 1 [label=su]
	2 [label=zag color=blue]
		0 -> 2 [label=ROOT]
	3 [label=hen]
		2 -> 3 [label=obj1]
	4 [label=wild]
		5 -> 4 [label=mod]
	5 [label=zwaaien color=green]
		2 -> 5 [label=vc]
	6 [label="."]
		5 -> 6 [label=punct]
}
'''.strip()

    def node_formatter(token):
        if token is None:
            return {'color': 'red'}
        elif token.cpos == 'N':
            return {'color': 'green'}
        elif token.cpos == 'V':
            return {'color': 'blue'}
        else:
            return {}
    sentence = Sentence.from_conll(conll_example.splitlines())
    dotgraph = sentence.as_dotgraph(node_formatter=node_formatter)
    assert dotgraph.source == formatted_dotgraph

def test_conll_as_dotgraph_custom_edgeformat():
    if older_than_py27: # this feature disabled in older Pythons
        return
    formatted_dotgraph = '''
digraph {
	0 [label=root]
	1 [label=Cathy]
		2 -> 1 [label=su color=blue]
	2 [label=zag]
		0 -> 2 [label=ROOT color=red]
	3 [label=hen]
		2 -> 3 [label=obj1 color=blue]
	4 [label=wild]
		5 -> 4 [label=mod color=blue]
	5 [label=zwaaien]
		2 -> 5 [label=vc color=blue]
	6 [label="."]
		5 -> 6 [label=punct color=blue]
}
'''.strip()

    sentence = Sentence.from_conll(conll_example.splitlines())
    def edge_formatter(token):
        if token.head == 0:
            return {'color': 'red'}
        else:
            return {'color': 'blue'}
    dotgraph = sentence.as_dotgraph(edge_formatter=edge_formatter)
    assert dotgraph.source == formatted_dotgraph

def test_read_sd_sentence():
    sample_deps = '''
det(burrito-2, A-1)
root(ROOT-0, burrito-2)
prep_with(burrito-2, beans-4)
prep_with(burrito-2, chicken-7)
conj_negcc(beans-4, chicken-7)
punct(burrito-2, .-8)
    '''.strip().splitlines()
    sentence = Sentence.from_stanford_dependencies(sample_deps, tree4)
    assert stringify_sentence(sentence) == tree4_out_CCprocessed

def test_read_sd_sentence_extra_space():
    sample_deps = '''

det(burrito-2, A-1)
root(ROOT-0, burrito-2)
prep_with(burrito-2, beans-4)
prep_with(burrito-2, chicken-7)
conj_negcc(beans-4, chicken-7)
punct(burrito-2, .-8)


    '''.splitlines()
    sentence = Sentence.from_stanford_dependencies(sample_deps, tree4)
    assert stringify_sentence(sentence) == tree4_out_CCprocessed

def test_read_sd_sentence_punct():
    sample_deps = '''
root(ROOT-0, Sentences-1)
punct(Sentences-1, :-2)
dep(Sentences-1, words-3)
punct(sometimes-8, -LRB--4)
prep(sometimes-8, with-5)
pobj(with-5, punctuation-6)
punct(sometimes-8, ---7)
dep(words-3, sometimes-8)
punct(sometimes-8, -RRB--9)
punct(Sentences-1, .-10)
    '''.strip().splitlines()
    tree = '''(ROOT (NP (NP (NNS Sentences)) (: :) (NP (NP (NNS words))
    (PRN (-LRB- -LRB-) (FRAG (PP (IN with) (NP (NN punctuation))) (: --)
    (ADVP (RB sometimes))) (-RRB- -RRB-))) (. .)))'''
    output = '''
Token(index=1, form='Sentences', cpos='NNS', pos='NNS', head=0, deprel='root')
Token(index=2, form=':', cpos=':', pos=':', head=1, deprel='punct')
Token(index=3, form='words', cpos='NNS', pos='NNS', head=1, deprel='dep')
Token(index=4, form='-LRB-', cpos='-LRB-', pos='-LRB-', head=8, deprel='punct')
Token(index=5, form='with', cpos='IN', pos='IN', head=8, deprel='prep')
Token(index=6, form='punctuation', cpos='NN', pos='NN', head=5, deprel='pobj')
Token(index=7, form='--', cpos=':', pos=':', head=8, deprel='punct')
Token(index=8, form='sometimes', cpos='RB', pos='RB', head=3, deprel='dep')
Token(index=9, form='-RRB-', cpos='-RRB-', pos='-RRB-', head=8, deprel='punct')
Token(index=10, form='.', cpos='.', pos='.', head=1, deprel='punct')
    '''.strip()

    sentence = Sentence.from_stanford_dependencies(sample_deps, tree)
    assert stringify_sentence(sentence) == output

    output_no_punct = '''
Token(index=1, form='Sentences', cpos='NNS', pos='NNS', head=0, deprel='root')
Token(index=3, form='words', cpos='NNS', pos='NNS', head=1, deprel='dep')
Token(index=5, form='with', cpos='IN', pos='IN', head=8, deprel='prep')
Token(index=6, form='punctuation', cpos='NN', pos='NN', head=5, deprel='pobj')
Token(index=8, form='sometimes', cpos='RB', pos='RB', head=3, deprel='dep')
    '''.strip()
    sentence2 = Sentence.from_stanford_dependencies(sample_deps, tree,
                                                    include_punct=False)
    assert stringify_sentence(sentence2) == output_no_punct

    sentence3 = Sentence.from_stanford_dependencies(sample_deps, tree,
                                                    include_punct=False,
                                                    include_erased=True)
    assert stringify_sentence(sentence3) == output_no_punct

    sentence4 = Sentence.from_stanford_dependencies(sample_deps, tree,
                                                    include_punct=True,
                                                    include_erased=True)
    assert stringify_sentence(sentence4) == output

    tree2 = '(ROOT(NP(NP-SBJ(NNS Sentences))(: :)(NP(NP(NNS words))(PRN(-LRB- -LRB-)(FRAG(PP(IN with)(NP(NN punctuation)))(: --)(ADVP(RB sometimes)))(-RRB- -RRB-)))(. .)))'
    sentence5 = Sentence.from_stanford_dependencies(sample_deps, tree2)
    assert sentence5 == sentence

    tree3 = '((NP(NP(NNS Sentences))(: :)(NP(NP(NNS words))(PRN(-LRB- -LRB-)(FRAG(PP(IN with)(NP(NN punctuation)))(: --)(ADVP(RB sometimes)))(-RRB- -RRB-)))(. .)))'
    sentence6 = Sentence.from_stanford_dependencies(sample_deps, tree3)
    assert sentence6 == sentence

    tree4 = ' ( ROOT(NP   ( NP-SBJ (NNS Sentences))(: :)(\nNP\n(NP(NNS\nwords)) (PRN (-LRB- -LRB-)(FRAG(PP    (IN with\n)\t(NP(NN punctuation )))(: --)(ADVP( RB sometimes )))(-RRB-    \t-RRB-)))(.\n\n\t.)))    '
    sentence7 = Sentence.from_stanford_dependencies(sample_deps, tree4)
    assert sentence7 == sentence

def test_read_sd_sentence_sorting():
    # same as test_read_sd_sentence but check sorting
    sample_deps = '''
punct(burrito-2, .-8)
conj_negcc(beans-4, chicken-7)
prep_with(burrito-2, chicken-7)
prep_with(burrito-2, beans-4)
root(ROOT-0, burrito-2)
det(burrito-2, A-1)
    '''.strip().splitlines()
    sentence = Sentence.from_stanford_dependencies(sample_deps, tree4)
    assert stringify_sentence(sentence) == tree4_out_CCprocessed

def test_read_sd_corpus_single():
    sample_deps = '''
det(burrito-2, A-1)
root(ROOT-0, burrito-2)
prep_with(burrito-2, beans-4)
prep_with(burrito-2, chicken-7)
conj_negcc(beans-4, chicken-7)
punct(burrito-2, .-8)
    '''.strip().splitlines()
    corpus = Corpus.from_stanford_dependencies(sample_deps, [tree4])
    assert len(corpus) == 1
    assert stringify_sentence(corpus[0]) == tree4_out_CCprocessed

def test_read_sd_corpus_multiple():
    sample_deps = '''
det(burrito-2, A-1)
root(ROOT-0, burrito-2)
prep_with(burrito-2, beans-4)
prep_with(burrito-2, chicken-7)
conj_negcc(beans-4, chicken-7)
punct(burrito-2, .-8)

nsubj(cooks-2, Ed-1)                          
nsubj(sells-4, Ed-1)
root(ROOT-0, cooks-2)
conj_and(cooks-2, sells-4)
dobj(cooks-2, burritos-5)
prep_with(burritos-5, beans-7)
prep_with(burritos-5, rice-10)
conj_negcc(beans-7, rice-10)
punct(cooks-2, .-11)
    '''.strip().splitlines()
    corpus = Corpus.from_stanford_dependencies(sample_deps, [tree4, tree5])
    assert len(corpus) == 2
    assert stringify_sentence(corpus[0]) == tree4_out_CCprocessed
    assert stringify_sentence(corpus[1]) == tree5_out_CCprocessed
