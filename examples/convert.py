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

# example code for converting trees to Universal/Stanford
# Dependencies. input is one tree per line. also useful for debugging
# PyStanfordDependencies.

from __future__ import print_function
import sys
import argparse
import fileinput
import StanfordDependencies

desc = '''Convert trees in files or stdin to Universal/Stanford
Dependencies.  Input is one tree per line. Also useful for debugging
PyStanfordDependencies.'''
parser = argparse.ArgumentParser(description=desc)
parser.add_argument('filenames', metavar='FILE', nargs='*',
                    help='Filenames to convert')
parser.add_argument('-b', '--backend', default='subprocess',
                    help='Backend to use (default: %(default)r)')
parser.add_argument('-r', '--representation', default='basic',
                    metavar='REPR',
                    help='Representation to use (default: %(default)r)')
parser.add_argument('-o', '--original', dest='universal',
                    action='store_false',
                    help="Don't use Universal Dependencies (if available)")
parser.add_argument('-V', '--corenlp-version', dest='version',
                    metavar='VERSION',
                    help="Version of CoreNLP (will use default if not set)")
parser.add_argument('-d', '--debug', action='store_true',
                    help="Enable debugging (subprocess only)")

args = parser.parse_args()
if args.debug:
    print('Args:', args)

conversion_args = dict(representation=args.representation,
                       universal=args.universal)
if args.debug:
    if args.backend == 'subprocess':
        conversion_args['debug'] = True
    else:
        print("Warning: Can only set debug flag in subprocess backend.",
              file=sys.stderr)

sd = StanfordDependencies.get_instance(backend=args.backend,
                                       version=args.version)
if not args.filenames: # interactive mode
    print("Ready to read and convert trees (one per line)")
for tree in fileinput.input(args.filenames):
    print('Tree: %r' % tree)
    tokens = sd.convert_tree(tree, **conversion_args)
    for token in tokens:
        print(token)
