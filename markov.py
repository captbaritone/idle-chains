from __future__ import print_function
from builtins import range
import os, random, nltk.data

class Markov(object):
    def __init__(self, corpus_file = None):
        if corpus_file is None:
            corpus_file = os.path.join(os.path.dirname(__file__), 'corpus.txt')
        self.cache = {}
        self.corpus_file = corpus_file
        self.words = self.file_to_words()
        self.word_size = len(self.words)
        self.database()

    def file_to_words(self):
        data = None
        with open(self.corpus_file) as corpus:
            data = corpus.read()
        words = data.split()
        return words

    def triples(self):
        """ Generates triples from the given data string. So if our string were
                "What a lovely day", we'd generate (What, a, lovely) and then
                (a, lovely, day).
        """

        if len(self.words) < 3:
            return

        for i in range(len(self.words) - 2):
            yield (self.words[i], self.words[i + 1], self.words[i + 2])

    def database(self):
        for w1, w2, w3 in self.triples():
            key = (w1, w2)
            if key in self.cache:
                self.cache[key].append(w3)
            else:
                self.cache[key] = [w3]

    def generate_markov_text(self, size=25):
        seed = random.randint(0, self.word_size - 3)
        seed_word, next_word = self.words[seed], self.words[seed + 1]
        w1, w2 = seed_word, next_word
        gen_words = []
        for i in range(size):
            gen_words.append(w1)
            w1, w2 = w2, random.choice(self.cache[(w1, w2)])
        gen_words.append(w2)
        return ' '.join(gen_words)

if __name__ == '__main__':
    m = Markov()
    text = m.generate_markov_text(300)
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    print(' '.join(sent_detector.tokenize(text.strip())[1:4]))
