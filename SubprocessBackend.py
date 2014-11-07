from StanfordDependencies import StanfordDependencies, Token
import subprocess
import tempfile

JAVA_CLASS_NAME = 'edu.stanford.nlp.trees.EnglishGrammaticalStructure'

class SubprocessBackend(StanfordDependencies):
    def __init__(self, jar_filename=None, java_command='java'):
        StanfordDependencies.__init__(self, jar_filename)
        self.java_command = java_command
    def convert_trees(self, ptb_trees, java='java', representation='basic'):
        """Convert a list of Penn Treebank formatted trees (ptb_trees)
        into Stanford Dependencies. The dependencies are represented
        as a list of sentences, where each sentence is itself a list of
        Token objects.

        Currently supported representations are 'basic', 'collapsed',
        'CCprocessed', and 'collapsedTree' which behave the same as they
        in the CoreNLP command line tools."""
        with tempfile.NamedTemporaryFile() as input_file:
            for ptb_tree in ptb_trees:
                input_file.write(ptb_tree + '\n')
            input_file.flush()

            command = [self.java_command, '-ea', '-cp', self.jar_filename,
                       JAVA_CLASS_NAME, '-' + representation, '-treeFile',
                       input_file.name, '-conllx']
            sd_process = subprocess.Popen(command, stdout=subprocess.PIPE)
            output = sd_process.stdout.read()

        current_sentence = []
        sentences = []
        def flush():
            if current_sentence:
                sentences.append(list(current_sentence))
                del current_sentence[:]
        for line in output.splitlines():
            line = line.strip()
            if line:
                current_sentence.append(Token.from_string(line))
            else:
                flush()
        flush()

        if len(sentences) != len(ptb_trees):
            raise RuntimeError("Only got %d sentences from Stanford Dependencies when given %d trees." % (len(sentences), len(ptb_trees)))
        return sentences
    def convert_tree(self, ptb_tree, **kwargs):
        """Converts a single Penn Treebank format tree to Stanford
        Dependencies. See convert_trees for more details."""
        return self.convert_trees([ptb_tree], **kwargs)[0]
