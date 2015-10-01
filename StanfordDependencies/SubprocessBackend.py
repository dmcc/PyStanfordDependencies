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
import os
import subprocess
import tempfile
from .StanfordDependencies import (StanfordDependencies,
                                   JavaRuntimeVersionError)
from .CoNLL import Corpus

JAVA_CLASS_NAME = 'edu.stanford.nlp.trees.EnglishGrammaticalStructure'

class SubprocessBackend(StanfordDependencies):
    """Interface to Stanford Dependencies via subprocesses. This means
    that each call opens a pipe to Java. It has the advantage that it
    should work out of the box if you have Java but it is slower than
    other backends. As such, convert_trees() will be more efficient than
    convert_tree() for this backend."""
    def __init__(self, jar_filename=None, download_if_missing=False,
                 version=None, java_command='java'):
        """java_command is the path to a java binary."""
        StanfordDependencies.__init__(self, jar_filename, download_if_missing,
                                      version)
        self.java_command = java_command
    def convert_trees(self, ptb_trees, representation='basic',
                      include_punct=True, include_erased=False, universal=True,
                      debug=False):
        """Convert a list of Penn Treebank formatted trees (ptb_trees)
        into Stanford Dependencies. The dependencies are represented
        as a list of sentences, where each sentence is itself a list of
        Token objects.

        Currently supported representations are 'basic', 'collapsed',
        'CCprocessed', and 'collapsedTree' which behave the same as they
        in the CoreNLP command line tools. (note that in the online
        CoreNLP demo, 'collapsed' is called 'enhanced')

        Setting debug=True will cause debugging information (including
        the java command run to be printed."""
        self._raise_on_bad_representation(representation)
        input_file = tempfile.NamedTemporaryFile(delete=False)
        try:
            for ptb_tree in ptb_trees:
                self._raise_on_bad_input(ptb_tree)
                tree_with_line_break = ptb_tree + "\n"
                input_file.write(tree_with_line_break.encode("utf-8"))
            input_file.flush()

            command = [self.java_command,
                       '-ea',
                       '-cp', self.jar_filename,
                       JAVA_CLASS_NAME,
                       '-' + representation,
                       '-treeFile', input_file.name]
            # if we're including erased, we want to include punctuation
            # since otherwise we won't know what SD considers punctuation
            if include_punct or include_erased:
                command.append('-keepPunct')
            if not universal:
                command.append('-originalDependencies')
            if debug:
                print('Command:', ' '.join(command))
            sd_process = subprocess.Popen(command, stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE,
                                          universal_newlines=True)
            return_code = sd_process.wait()
            stderr = sd_process.stderr.read()
            stdout = sd_process.stdout.read()

            if debug:
                print("stdout: {%s}" % stdout)
                print("stderr: {%s}" % stderr)
                print('Exit code:', return_code)

            self._raise_on_bad_exit_or_output(return_code, stderr)
        finally:
            os.remove(input_file.name)

        try:
            sentences = Corpus.from_stanford_dependencies(stdout.splitlines(),
                                                          ptb_trees,
                                                          include_erased,
                                                          include_punct)
            for sentence, ptb_tree in zip(sentences, ptb_trees):
                if len(sentence) == 0:
                    raise ValueError("Invalid PTB tree: %r" % ptb_tree)
        except:
            print("Error during conversion")
            if not debug:
                print("stdout: {%s}" % stdout)
                print("stderr: {%s}" % stderr)
            raise

        assert len(sentences) == len(ptb_trees), \
            "Only got %d sentences from Stanford Dependencies when " \
            "given %d trees." % (len(sentences), len(ptb_trees))
        return sentences
    def convert_tree(self, ptb_tree, **kwargs):
        """Converts a single Penn Treebank formatted tree (a string)
        to Stanford Dependencies. See convert_trees for more details."""
        return self.convert_trees([ptb_tree], **kwargs)[0]

    @staticmethod
    def _raise_on_bad_exit_or_output(return_code, stderr):
        if 'PennTreeReader: warning:' in stderr:
            raise ValueError("Tree(s) not in valid Penn Treebank format")

        if return_code:
            if 'Unsupported major.minor version' in stderr:
                # Oracle Java error message
                raise JavaRuntimeVersionError()
            elif 'JVMCFRE003 bad major version' in stderr:
                # IBM Java error message
                raise JavaRuntimeVersionError()
            else:
                raise ValueError("Bad exit code from Stanford CoreNLP")
