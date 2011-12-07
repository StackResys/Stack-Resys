import sys
import string

def has_bad_chars(word):
    bad_characters = "()"
    for bad_char in bad_characters:
        if bad_char in word:
            return True
    return False

def has_no_letter(word):
    return all(char not in string.letters for char in word)

def normalize_word(word):
    if has_bad_chars(word) or has_no_letter(word):
        return ""

    return word.lower()

def normalized(source):
    for line in source:
        words = set([word.lower() for word in line[:-1].split('\t') \
                     if not has_bad_chars(word)])
        if len(words) < 2:
            yield ""
        else:
            yield "\t".join(words)

if __name__ == "__main__":
    SOURCE = sys.stdin if len(sys.argv) < 2 else open(sys.argv[1])
    for line in normalized(SOURCE):
        if line != "":
            print line

