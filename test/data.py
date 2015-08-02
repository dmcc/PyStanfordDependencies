# this file contains all the string data (inputs and outputs) for tests

# the SD trees were originally produced on SD 3.4.1 but they work up
# to (at least) SD 3.5.2. the UD trees were produced using UD 3.5.2.
# tests now require SD/UD 3.5.2 (and thus Java 1.8). downside of this
# is that we can't test JPype on older versions of SD since it can only
# be (safely) initialized once.

class trees_sd:
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
    tree5_out_collapsedTree_no_punct = '''
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

    # tests -NONE- handling
    tree6 = '''
( (S 
    (S-TPC-1 
      (NP-SBJ (PRP He) )
      (ADVP (RB also) )
      (VP (VBZ is) 
        (NP-PRD (DT a) (NN consensus) (NN manager) )))
    (, ,) 
    (NP-SBJ (NNS insiders) )
    (VP (VBP say) 
      (SBAR (-NONE- 0) 
        (S (-NONE- *T*-1) )))
    (. .) ))
    '''
    tree6_out = '''
Token(index=1, form='He', cpos='PRP', pos='PRP', head=6, deprel='nsubj')
Token(index=2, form='also', cpos='RB', pos='RB', head=6, deprel='advmod')
Token(index=3, form='is', cpos='VBZ', pos='VBZ', head=6, deprel='cop')
Token(index=4, form='a', cpos='DT', pos='DT', head=6, deprel='det')
Token(index=5, form='consensus', cpos='NN', pos='NN', head=6, deprel='nn')
Token(index=6, form='manager', cpos='NN', pos='NN', head=9, deprel='ccomp')
Token(index=7, form=',', cpos=',', pos=',', head=9, deprel='punct')
Token(index=8, form='insiders', cpos='NNS', pos='NNS', head=9, deprel='nsubj')
Token(index=9, form='say', cpos='VBP', pos='VBP', head=0, deprel='root')
Token(index=10, form='.', cpos='.', pos='.', head=9, deprel='punct')
'''.strip()

    # tests weird \/ handling
    tree7 = '''(S1 (NP 
(NP (NNP PRIME) (NNP RATE) )
(: :) 
(NP (CD 10) (CD 1\/2) (NN %) )
(. .) ))'''
    tree7_out = '''
Token(index=1, form='PRIME', cpos='NNP', pos='NNP', head=2, deprel='nn')
Token(index=2, form='RATE', cpos='NNP', pos='NNP', head=0, deprel='root')
Token(index=3, form=':', cpos=':', pos=':', head=2, deprel='punct')
Token(index=4, form='10', cpos='CD', pos='CD', head=6, deprel='num')
Token(index=5, form='1/2', cpos='CD', pos='CD', head=6, deprel='num')
Token(index=6, form='%', cpos='NN', pos='NN', head=2, deprel='dep')
Token(index=7, form='.', cpos='.', pos='.', head=2, deprel='punct')
    '''.strip()

    @classmethod
    def get_basic_test_trees(self):
        return ((self.tree1, self.tree1_out), (self.tree2, self.tree2_out_basic),
                (self.tree3, self.tree3_out), (self.tree4, self.tree4_out_basic),
                (self.tree5, self.tree5_out_basic), (self.tree6, self.tree6_out),
                (self.tree7, self.tree7_out))
    @classmethod
    def get_repr_test_tree2(self):
        return sorted(dict(basic=self.tree2_out_basic, collapsed=self.tree2_out_collapsed,
                           CCprocessed=self.tree2_out_CCprocessed,
                           collapsedTree=self.tree2_out_collapsedTree).items())
    @classmethod
    def get_repr_test_tree4(self):
        return sorted(dict(basic=self.tree4_out_basic, collapsed=self.tree4_out_collapsed,
                      CCprocessed=self.tree4_out_CCprocessed,
                      collapsedTree=self.tree4_out_collapsedTree).items())
    @classmethod
    def get_repr_test_tree5(self):
        return sorted(dict(basic=self.tree5_out_basic, collapsed=self.tree5_out_collapsed,
                           CCprocessed=self.tree5_out_CCprocessed,
                           collapsedTree=self.tree5_out_collapsedTree).items())

# UD trees are similar to SD trees, but some parts are overridden
class trees_ud(trees_sd):
    tree2_out_collapsed = '''
Token(index=1, form='A', cpos='DT', pos='DT', head=2, deprel='det')
Token(index=2, form='cat', cpos='NN', pos='NN', head=0, deprel='root')
Token(index=3, form='and', cpos='CC', pos='CC', head=2, deprel='cc')
Token(index=4, form='a', cpos='DT', pos='DT', head=5, deprel='det')
Token(index=5, form='mouse', cpos='NN', pos='NN', head=2, deprel='conj:and')
Token(index=6, form='.', cpos='.', pos='.', head=2, deprel='punct')
    '''.strip()
    tree2_out_collapsedTree = tree2_out_collapsed
    tree2_out_CCprocessed = tree2_out_collapsed

    tree4_out_basic = '''
Token(index=1, form='A', cpos='DT', pos='DT', head=2, deprel='det')
Token(index=2, form='burrito', cpos='NN', pos='NN', head=0, deprel='root')
Token(index=3, form='with', cpos='IN', pos='IN', head=4, deprel='case')
Token(index=4, form='beans', cpos='NNS', pos='NNS', head=2, deprel='nmod')
Token(index=5, form='but', cpos='CC', pos='CC', head=6, deprel='cc')
Token(index=6, form='not', cpos='RB', pos='RB', head=4, deprel='cc')
Token(index=7, form='chicken', cpos='NN', pos='NN', head=4, deprel='conj')
Token(index=8, form='.', cpos='.', pos='.', head=2, deprel='punct')
    '''.strip()
    tree4_out_collapsed = '''
Token(index=1, form='A', cpos='DT', pos='DT', head=2, deprel='det')
Token(index=2, form='burrito', cpos='NN', pos='NN', head=0, deprel='root')
Token(index=3, form='with', cpos='IN', pos='IN', head=4, deprel='case')
Token(index=4, form='beans', cpos='NNS', pos='NNS', head=2, deprel='nmod:with')
Token(index=5, form='but', cpos='CC', pos='CC', head=6, deprel='cc')
Token(index=6, form='not', cpos='RB', pos='RB', head=4, deprel='cc')
Token(index=7, form='chicken', cpos='NN', pos='NN', head=4, deprel='conj:negcc')
Token(index=8, form='.', cpos='.', pos='.', head=2, deprel='punct')
    '''.strip()
    tree4_out_CCprocessed = '''
Token(index=1, form='A', cpos='DT', pos='DT', head=2, deprel='det')
Token(index=2, form='burrito', cpos='NN', pos='NN', head=0, deprel='root')
Token(index=3, form='with', cpos='IN', pos='IN', head=4, deprel='case')
Token(index=4, form='beans', cpos='NNS', pos='NNS', head=2, deprel='nmod:with')
Token(index=5, form='but', cpos='CC', pos='CC', head=6, deprel='cc')
Token(index=6, form='not', cpos='RB', pos='RB', head=4, deprel='cc')
Token(index=7, form='chicken', cpos='NN', pos='NN', head=2, deprel='nmod:with')
Token(index=7, form='chicken', cpos='NN', pos='NN', head=4, deprel='conj:negcc')
Token(index=8, form='.', cpos='.', pos='.', head=2, deprel='punct')
    '''.strip()
    tree4_out_collapsedTree = tree4_out_collapsed

    tree5_out_basic = '''
Token(index=1, form='Ed', cpos='NNP', pos='NNP', head=2, deprel='nsubj')
Token(index=2, form='cooks', cpos='VBZ', pos='VBZ', head=0, deprel='root')
Token(index=3, form='and', cpos='CC', pos='CC', head=2, deprel='cc')
Token(index=4, form='sells', cpos='VBZ', pos='VBZ', head=2, deprel='conj')
Token(index=5, form='burritos', cpos='NNS', pos='NNS', head=2, deprel='dobj')
Token(index=6, form='with', cpos='IN', pos='IN', head=7, deprel='case')
Token(index=7, form='beans', cpos='NNS', pos='NNS', head=5, deprel='nmod')
Token(index=8, form='but', cpos='CC', pos='CC', head=9, deprel='cc')
Token(index=9, form='not', cpos='RB', pos='RB', head=7, deprel='cc')
Token(index=10, form='rice', cpos='NN', pos='NN', head=7, deprel='conj')
Token(index=11, form='.', cpos='.', pos='.', head=2, deprel='punct')
    '''.strip()
    tree5_out_collapsed = '''
Token(index=1, form='Ed', cpos='NNP', pos='NNP', head=2, deprel='nsubj')
Token(index=2, form='cooks', cpos='VBZ', pos='VBZ', head=0, deprel='root')
Token(index=3, form='and', cpos='CC', pos='CC', head=2, deprel='cc')
Token(index=4, form='sells', cpos='VBZ', pos='VBZ', head=2, deprel='conj:and')
Token(index=5, form='burritos', cpos='NNS', pos='NNS', head=2, deprel='dobj')
Token(index=6, form='with', cpos='IN', pos='IN', head=7, deprel='case')
Token(index=7, form='beans', cpos='NNS', pos='NNS', head=5, deprel='nmod:with')
Token(index=8, form='but', cpos='CC', pos='CC', head=9, deprel='cc')
Token(index=9, form='not', cpos='RB', pos='RB', head=7, deprel='cc')
Token(index=10, form='rice', cpos='NN', pos='NN', head=7, deprel='conj:negcc')
Token(index=11, form='.', cpos='.', pos='.', head=2, deprel='punct')
    '''.strip()
    tree5_out_CCprocessed = '''
Token(index=1, form='Ed', cpos='NNP', pos='NNP', head=2, deprel='nsubj')
Token(index=1, form='Ed', cpos='NNP', pos='NNP', head=4, deprel='nsubj')
Token(index=2, form='cooks', cpos='VBZ', pos='VBZ', head=0, deprel='root')
Token(index=3, form='and', cpos='CC', pos='CC', head=2, deprel='cc')
Token(index=4, form='sells', cpos='VBZ', pos='VBZ', head=2, deprel='conj:and')
Token(index=5, form='burritos', cpos='NNS', pos='NNS', head=2, deprel='dobj')
Token(index=6, form='with', cpos='IN', pos='IN', head=7, deprel='case')
Token(index=7, form='beans', cpos='NNS', pos='NNS', head=5, deprel='nmod:with')
Token(index=8, form='but', cpos='CC', pos='CC', head=9, deprel='cc')
Token(index=9, form='not', cpos='RB', pos='RB', head=7, deprel='cc')
Token(index=10, form='rice', cpos='NN', pos='NN', head=5, deprel='nmod:with')
Token(index=10, form='rice', cpos='NN', pos='NN', head=7, deprel='conj:negcc')
Token(index=11, form='.', cpos='.', pos='.', head=2, deprel='punct')
    '''.strip()
    tree5_out_collapsedTree = tree5_out_collapsed

    tree5_out_collapsedTree_no_punct = '''
Token(index=1, form='Ed', cpos='NNP', pos='NNP', head=2, deprel='nsubj')
Token(index=2, form='cooks', cpos='VBZ', pos='VBZ', head=0, deprel='root')
Token(index=3, form='and', cpos='CC', pos='CC', head=2, deprel='cc')
Token(index=4, form='sells', cpos='VBZ', pos='VBZ', head=2, deprel='conj:and')
Token(index=5, form='burritos', cpos='NNS', pos='NNS', head=2, deprel='dobj')
Token(index=6, form='with', cpos='IN', pos='IN', head=7, deprel='case')
Token(index=7, form='beans', cpos='NNS', pos='NNS', head=5, deprel='nmod:with')
Token(index=8, form='but', cpos='CC', pos='CC', head=9, deprel='cc')
Token(index=9, form='not', cpos='RB', pos='RB', head=7, deprel='cc')
Token(index=10, form='rice', cpos='NN', pos='NN', head=7, deprel='conj:negcc')
    '''.strip()

    # nothing gets erased in UD
    tree5_out_collapsedTree_erased = tree5_out_collapsedTree
    tree5_out_collapsedTree_erased_no_punct = tree5_out_collapsedTree_no_punct

    tree5_out_basic_lemmas = '''
Token(index=1, form='Ed', lemma='Ed', cpos='NNP', pos='NNP', head=2, deprel='nsubj')
Token(index=2, form='cooks', lemma='cook', cpos='VBZ', pos='VBZ', head=0, deprel='root')
Token(index=3, form='and', lemma='and', cpos='CC', pos='CC', head=2, deprel='cc')
Token(index=4, form='sells', lemma='sell', cpos='VBZ', pos='VBZ', head=2, deprel='conj')
Token(index=5, form='burritos', lemma='burrito', cpos='NNS', pos='NNS', head=2, deprel='dobj')
Token(index=6, form='with', lemma='with', cpos='IN', pos='IN', head=7, deprel='case')
Token(index=7, form='beans', lemma='bean', cpos='NNS', pos='NNS', head=5, deprel='nmod')
Token(index=8, form='but', lemma='but', cpos='CC', pos='CC', head=9, deprel='cc')
Token(index=9, form='not', lemma='not', cpos='RB', pos='RB', head=7, deprel='cc')
Token(index=10, form='rice', lemma='rice', cpos='NN', pos='NN', head=7, deprel='conj')
Token(index=11, form='.', lemma='.', cpos='.', pos='.', head=2, deprel='punct')
    '''.strip()

    tree6_out = '''
Token(index=1, form='He', cpos='PRP', pos='PRP', head=6, deprel='nsubj')
Token(index=2, form='also', cpos='RB', pos='RB', head=6, deprel='advmod')
Token(index=3, form='is', cpos='VBZ', pos='VBZ', head=6, deprel='cop')
Token(index=4, form='a', cpos='DT', pos='DT', head=6, deprel='det')
Token(index=5, form='consensus', cpos='NN', pos='NN', head=6, deprel='compound')
Token(index=6, form='manager', cpos='NN', pos='NN', head=9, deprel='ccomp')
Token(index=7, form=',', cpos=',', pos=',', head=9, deprel='punct')
Token(index=8, form='insiders', cpos='NNS', pos='NNS', head=9, deprel='nsubj')
Token(index=9, form='say', cpos='VBP', pos='VBP', head=0, deprel='root')
Token(index=10, form='.', cpos='.', pos='.', head=9, deprel='punct')
'''.strip()

    tree7_out = '''
Token(index=1, form='PRIME', cpos='NNP', pos='NNP', head=2, deprel='compound')
Token(index=2, form='RATE', cpos='NNP', pos='NNP', head=0, deprel='root')
Token(index=3, form=':', cpos=':', pos=':', head=2, deprel='punct')
Token(index=4, form='10', cpos='CD', pos='CD', head=6, deprel='nummod')
Token(index=5, form='1/2', cpos='CD', pos='CD', head=6, deprel='nummod')
Token(index=6, form='%', cpos='NN', pos='NN', head=2, deprel='dep')
Token(index=7, form='.', cpos='.', pos='.', head=2, deprel='punct')
    '''.strip()

