import bayesianClassifier
import config
import os
import sys

def read_meta_data(path, threshold):
    result = {}
    for line in open(path):
        parts = line[:-1].split(":")
        count = int(parts[2])
        if count < threshold:
            continue
        result[int(parts[0])] = (parts[1], count)
    return result

def to_ints(array, filter = lambda x: True):
    raw = (int(elem) for elem in array if len(elem) > 0)
    return tuple(elem for elem in raw if filter(elem))

def get_named_tags(tags, all_tags):
    return [all_tags[tag][0] for tag in tags]

if __name__ == "__main__":
    # Read meta-data
    conf = config.INPUT
    word_threshold = conf["word_threshold"]
    tag_threshold = conf["tag_threshold"]
    data_path = conf["data_path"]

    all_tags = read_meta_data(os.path.join(data_path, "tags.stat"),
                          tag_threshold)
    all_words = read_meta_data(os.path.join(data_path, "words.stat"),
                           word_threshold)

    # Training
    conf = config.CLASSIFIER
    classifier = bayesianClassifier.BayesianClassifier(conf["beta"])

    lines = enumerate(open(os.path.join(data_path, "vectors.stat")))
    for index, line in lines:
        if index > 20000:
            break
        if index % 200 == 0:
            print "."
            sys.stdout.flush()
        segments = line[:-1].split(';')
        tags = to_ints(segments[1].split(), lambda t: t in all_tags)
        words = (to_ints(elem.split(":"))
                for elem in segments[0].split())
        words = dict(elem for elem in words if (elem[0] in all_words))

        classifier.train(words, tags)

    for index, line in lines:
        if index > 20015:
            break
        segments = line[:-1].split(';')
        tags = to_ints(segments[1].split(), lambda t: t in all_tags)
        words = (to_ints(elem.split(":"))
                for elem in segments[0].split())
        words = dict(elem for elem in words if (elem[0] in all_words))

        print "Expected:", get_named_tags(tags, all_tags)
        actual = classifier.classify(words)
        expected_tags = (tag for tag, score in actual[:10])
        dic = {}
        for index, item in enumerate(actual):
            dic[item[0]] = (item[1], index)

        print "Actual:", get_named_tags(expected_tags, all_tags)
        print "Rank:", [(w, dic[w][1]) for w in tags if w in dic]


