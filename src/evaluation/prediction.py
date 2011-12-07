import config
import os
import naive_bayes
import sys
from log import LOGGER
import persistence

# -- READING Basic Info
def read_tags_and_words():
    """ Read tags and words by the configuration """
    conf = config.INPUT
    base_path = conf["base_path"]
    tag_threshold = conf["tag_threshold"]
    word_threshold = conf["word_threshold"]

    tags_info = read_meta_data(
            os.path.join(base_path, "tags.stat"),
            tag_threshold)
    words_info = read_meta_data(
            os.path.join(base_path, "words.stat"),
            word_threshold)

    return tags_info, words_info

def read_meta_data(path, threshold):
    """ Utility function used for reading the
        word count or tag count """
    result = {}
    for line in open(path):
        parts = line[:-1].split(":")
        count = int(parts[2])
        if count < threshold:
            continue
        result[int(parts[0])] = (parts[1], count)
    return result

# -- Utilities
def to_ints(array, filter = lambda x: True):
    """ Convert a string list to an int list """
    raw = (int(elem) for elem in array if len(elem) > 0)
    return tuple(elem for elem in raw if filter(elem))

def get_predicted_results_from_file(filename):
    for line in open(filename):
        parts = line.split(';')
        original = to_ints(parts[0].split())
        predicted = [tags_info.split(':')[0] for tags_info in parts[1].split()]
        scores = [float(tags_info.split(':')[0]) for tags_info in parts[1].split()]
        predicted = to_ints(predicted)
        yield original, zip(predicted, scores)

#
def get_test_samples():
    """ Get the iterator of the test data """
    path = os.path.join(config.INPUT["base_path"], "test.stat")
    return open(path)

def get_sample_results_by_naive_bayes(classifier, tags_info, words_info):
    """ This generator will read the test samples and
        return a sequence of predicted results.  """
    LOGGER.info("Creating the naive bayes classifier...")
    classifier = create_classifier(tags_info, words_info)

    # Getting the test samples
    LOGGER.info("Start to process the samples")
    test_samples = get_test_samples()

    # Start to process the test samples
    for line in test_samples:
        LOGGER.info("Processing sample...")

        # -- Parse the records
        # Each line of the sample is make up by three parts
        #   - id
        #   - words
        #   - tags
        # A typical line will look like this:
        #   question_id;word_id1:count<tag>word_id2:count;tag_id1<tab>tag_id2
        segments = line[:-1].split(';')
        words = (to_ints(elem.split(":"))
                for elem in segments[1].split())
        words = dict(elem for elem in words if (elem[0] in words_info))
        tags = to_ints(segments[2].split(), lambda t: t in tags_info)

        # -- Classifying
        LOGGER.info("Classifying sample %s..." % segments[0])
        tags_with_score = classifier.classify(words)

        yield tags, tags_with_score

def make_classifier_from_config(all_tags, all_words):
    """ Create a naive classifier from scratch """
    # Training
    conf = config.CLASSIFIER
    base_path = config.INPUT["base_path"]
    classifier = naive_bayes.Classifier(conf["beta"])

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

def create_classifier(all_tags, all_words):
    LOGGER.debug("Creating classifier ...")
    conf = config.INPUT
    base_path = conf["base_path"]
    model_path = os.path.join(base_path, "bayes.model")

    # Create classifier from scratch or from already persisted model
    if not config.CLASSIFIER["retrain_model"] and os.path.exists(model_path):
        LOGGER.debug("Creating classifier from file ...")
        classifier = persistence.load_model(model_path)
        LOGGER.debug("Reading completed.")
    else:
        LOGGER.debug("Creating empty classifier ...")
        classifier = make_classifier_from_config(all_tags, all_words)
        LOGGER.debug("Traing completed.")

    if config.CLASSIFIER["retrain_model"]:
        LOGGER.debug("Writing the model to %s ..." % model_path)
        persistence.save_model(classifier, model_path)
        LOGGER.debug("Writing model completed.")
    return classifier
