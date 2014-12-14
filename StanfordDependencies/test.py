#!/usr/bin/env python
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

from StanfordDependencies import StanfordDependencies

def print_sentences(sentences):
    for sentence in sentences:
        print '---'
        for token in sentence:
            print token
    print

if __name__ == "__main__":
    # simple testing script -- ideally will be replaced with proper
    # unit tests

    for backend in ('jpype', 'subprocess'):
        print 'Backend:', backend
        sd = StanfordDependencies.get_instance(backend=backend)
        sents = sd.convert_trees(['(S1 (NP (DT a) (NN cow)))',
                                  '(S1 (NP (DT some) (NNS cows)))',
                                  '(S1 (NP (DT some) (JJ blue) (NN moose)))'],
                                 representation='basic')
        print_sentences(sents)

        tree = '(S1 (NP (NP (NP (DT A) (NN cat)) (CC and) ' + \
               '(NP (DT a) (NN mouse))) (. .)))'
        for representation in ('basic', 'collapsed', 'CCprocessed',
                               'collapsedTree'):
            print '%s representation' % representation
            print_sentences(sd.convert_trees([tree],
                                             representation=representation))
