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

# example code for converting trees to Stanford Dependencies.
# input is one tree per line. by default, uses subprocess backend,
# the latest version of UD, and prints debugging information.

from __future__ import print_function
import fileinput
import StanfordDependencies
sd = StanfordDependencies.get_instance(backend='subprocess')
for tree in fileinput.input():
    print('Tree:', tree)
    tokens = sd.convert_tree(tree, representation='collapsed', universal=True, debug=True)
    for token in tokens:
        print(token)
