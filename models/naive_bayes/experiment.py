import bayesianClassifier
import config
import os
import sys
import persistence

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

def make_configured_classifier(all_tags, all_words):
    # Read meta-data
    conf = config.INPUT

    # Training
    conf = config.CLASSIFIER
    classifier = bayesianClassifier.BayesianClassifier(conf["beta"])

    train_count = conf["train_count"]
    lines = enumerate(open(os.path.join(base_path, "train.stat")))
    for index, line in lines:
        if index > train_count:
            break
        if index % 500 == 0 and index != 0:
            print ".",
            sys.stdout.flush()
        if index % 5000 == 0 and index != 0:
            print "\n"
            sys.stdout.flush()
        segments = line[:-1].split(';')
        tags = to_ints(segments[2].split(), lambda t: t in all_tags)
        words = (to_ints(elem.split(":"))
                for elem in segments[1].split())
        words = dict(elem for elem in words if (elem[0] in all_words))

        classifier.train(words, tags)
    return classifier

if __name__ == "__main__":
    base_path = config.INPUT["base_path"]
    # Readings
    conf = config.INPUT
    tag_threshold = conf["tag_threshold"]
    word_threshold = conf["word_threshold"]
    all_tags = read_meta_data(os.path.join(base_path, "tags.stat"),
                          tag_threshold)
    all_words = read_meta_data(os.path.join(base_path, "words.stat"),
                           word_threshold)

    model_path = os.path.join(base_path, "bayes.model")
    if not config.CLASSIFIER["rewrite_model"] and os.path.exists(model_path):
        classifier = persistence.load(model_path)
    else:
        classifier = make_configured_classifier(all_tags, all_words)

    if config.CLASSIFIER["rewrite_model"]:
        print "\nPersistence"
        persistence.save(classifier, model_path)

    # -- Test
    lines = enumerate(open(os.path.join(base_path, "test.stat")))
    test_count = config.CLASSIFIER["test_count"]
    for index, line in lines:
        if index > test_count:
            break
        segments = line[:-1].split(';')
        tags = to_ints(segments[2].split(), lambda t: t in all_tags)
        words = (to_ints(elem.split(":"))
                for elem in segments[1].split())
        words = dict(elem for elem in words if (elem[0] in all_words))

        print "\n------\nId:", segments[0]
        print "Expected:", get_named_tags(tags, all_tags)
        scores = classifier.classify(words)
        actual_tags = (s for s, c in scores[:10])
        dic = {}
        for index, item in enumerate(scores):
            dic[item[0]] = (item, index)

        print "Actual:", get_named_tags(actual_tags, all_tags)
        print "Scores:", [c for s, c in scores[:10]]
        print "Rank:", [(all_tags[w][0], dic[w]) for w in tags if w in dic]



