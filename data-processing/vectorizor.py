import config
import re

class Vectorizor:
    """ Converting a document to the word vector """
    def __init__(self, tags = {}, words = {}, stop_words = []):
        # statistical information
        self.tags = tags
        self.words = words
        self.stop_words = stop_words

        # Misc
        self.word_matcher = re.compile(
                "[\w\d+#@$]{2,8}[a-zA-Z][\w\d+#@$]{2,8}")

    def vectorize(self, doc, tags):
        normalized_tags = self._normalize_tags(tags)
        vector = {}
        for word in self._split_words(doc):
            if word in self.stop_words:
                continue
            word_id = self._update_word(word)[0]
            vector.setdefault(word_id, 0)
            vector[word_id] += 1
        return vector, normalized_tags

    # Update statistical information
    def _normalize_tags(self, tags):
        normalized_tag = []
        for tag in tags:
            # update the statistical info
            item = self._update_elem(tag, self.tags)
            normalized_tag.append(item[0])
        return normalized_tag

    def _update_word(self, word):
        return self._update_elem(word, self.words)

    def _update_elem(self, elem, elems, count = 1):
        item = elems.setdefault(elem, [len(elems), 0])
        item[1] += count
        return item

    def _split_words(self, doc):
        return self.word_matcher.findall(doc.lower())

