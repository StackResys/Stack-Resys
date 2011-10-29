import config
import re

class Vectorizor:
    """ Converting a document to the word vector """
    def __init__(self, stop_words = []):
        # statistical information
        self.tags = {}
        self.tag_count = {}

        self.words = {}
        self.word_count = {}

        self.stop_words = stop_words

        # Misc
        self.word_matcher = re.compile("[\w\d+#@$']{2,15}")

    def vectorize(self, doc, tags):
        self._update_tags(tags)
        vector = {}
        for word in self._split_words(doc):
            if word in self.stop_words:
                continue
            self._update_word(word)
            vector.setdefault(word, 0)
            vector[word] += 1
        return vector

    # Update statistical information
    def _update_tags(self, tags):
        for tag in tags:
            self._update_elem(tag, self.tags, self.tag_count)

    def _update_word(self, word):
        self._update_elem(word, self.words, self.word_count)

    def _update_elem(self, elem, elems, elem_count, count = 1):
        if elem not in elems:
            elems[elem] = len(elems)
            elem_count[elem] = 0
        elem_count[elem] += count

    def _split_words(self, doc):
        return self.word_matcher.findall(doc.lower())

