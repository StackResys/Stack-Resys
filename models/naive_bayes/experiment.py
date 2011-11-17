import bayesianClassifier
import config
from log import logger
import os
import persistence
import sys

# -- READING Basic Info
def read_tags_and_words():
    conf = config.INPUT
    base_path = conf["base_path"]
    tag_threshold = conf["tag_threshold"]
    word_threshold = conf["word_threshold"]

    all_tags = read_meta_data(os.path.join(base_path, "tags.stat"),
                          tag_threshold)
    all_words = read_meta_data(os.path.join(base_path, "words.stat"),
                           word_threshold)

    return all_tags, all_words

def read_meta_data(path, threshold):
    result = {}
    for line in open(path):
        parts = line[:-1].split(":")
        count = int(parts[2])
        if count < threshold:
            continue
        result[int(parts[0])] = (parts[1], count)
    return result

# -- Create Classifier
def create_classifier():
    logger.debug("Creating classifier ...")
    conf = config.INPUT
    base_path = conf["base_path"]
    model_path = os.path.join(base_path, "bayes.model")

    # Create classifier from scratch or from already persisted model
    if not config.CLASSIFIER["retrain_model"] and os.path.exists(model_path):
        logger.debug("Creating classifier from file ...")
        classifier = persistence.load_model(model_path)
        logger.debug("Reading completed.")
    else:
        logger.debug("Creating empty classifier ...")
        classifier = make_classifier_from_config(all_tags, all_words)
        logger.debug("Traing completed.")

    if config.CLASSIFIER["retrain_model"]:
        logger.debug("Writing the model to %s ..." % model_path)
        persistence.save_model(classifier, model_path)
        logger.debug("Writing model completed.")
    return classifier

def make_classifier_from_config(all_tags, all_words):
    # Training
    conf = config.CLASSIFIER
    base_path = config.INPUT["base_path"]
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

# Testing Data
def run_test(classifier):
    base_path = config.INPUT["base_path"]

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

        logger.info("Test %d: %s" % (index, segments[0]))
        logger.info("Classifying...")
        scores = classifier.classify(words)
        actual_tags = (s for s, c in scores[:10])
        dic = {}
        for index, item in enumerate(scores):
            dic[item[0]] = (item, index)

        test_result = """
          Expected: %s
          Predicted: %s
          Rank: %s
        """ % (
            str(get_tag_name(tags, all_tags)),
            str(get_tag_name(actual_tags, all_tags)),
            str([(all_tags[w][0], dic[w][1]) for w in tags if w in dic]))
        logger.info(test_result)

# -- Utilities
def to_ints(array, filter = lambda x: True):
    raw = (int(elem) for elem in array if len(elem) > 0)
    return tuple(elem for elem in raw if filter(elem))

def get_tag_name(tags, all_tags):
    return [all_tags[tag][0] for tag in tags]


if __name__ == "__main__":
    all_tags, all_words = read_tags_and_words()
    classifier = create_classifier()
    run_test(classifier)


