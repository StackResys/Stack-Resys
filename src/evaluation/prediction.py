import config
import os
from log import LOGGER
import persistence
import naive_bayes

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

def get_test_samples():
    """ Get the iterator of the test data """
    path = os.path.join(config.INPUT["base_path"], "test.stat")
    return open(path)

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

def get_evaluation_from_file(pipeline_name):
    tags_info, words_info = read_tags_and_words()
    test_samples = get_predicted_results_from_file("../../data/test_results/knnResult.txt")
    sample_count = config.CLASSIFIER["sample_count"]

    pipeline = config.PIPELINES[pipeline_name]
    # TODO extend from naive bayes to any classifier
    classifier = create_classifier(tags_info, words_info)
    # TODO Please note that not all the evaluator's constructor looks like this
    evaluator1 = pipeline["evaluator"](classifier.label_counts, \
                                      classifier.label_feature_count, \
                                      pipeline["evaluator_file"])

    base_path = config.INPUT["base_path"]
    basket_info_file = os.path.join(base_path, "basket.stat")
    train_data_file = os.path.join(base_path, "vectors.stat")

    evaluator2 = BasketEvaluator(basket_info_file, train_data_file)

    r_tags = rev(tags_info)

    # run the test
    for index, line in enumerate(test_samples):
        # Parse the records
        LOGGER.info("Classifying...")

        expected, actual = line
        print expected
        print actual
        print "r_tags", len(r_tags), r_tags.items()[0]
        etags = [r_tags[tag] for tag in expected if tag in r_tags]
        atags = [r_tags[tag] for tag in actual if tag in r_tags]

        print "Basket:", evaluator1.update(atags, etags)
        print "KL-distance", evaluator2.update(atags, etags)

        """
        test_result =
        (
            str(expected),
            str(actual),
            str([(tags_info[w][0], dic[w][1]) for w in tags if w in dic]))
        LOGGER.info(test_result)
        """
    LOGGER.info(str(evaluator1.get_evaluation()))
    LOGGER.info(str(evaluator2.get_evaluation()))

def rev(d):
    result = {}
    for key, val in d.items():
        result[val[0]] = key
    return result

# TODO -- This is a hack
def get_sample_results_by_naive_bayes(tags_info, words_info, evaluator = None):
    """ This generator will read the test samples and
        return a sequence of predicted results.  """
    LOGGER.info("Creating the naive bayes classifier...")
    classifier = create_classifier(tags_info, words_info)

    # TODO: HACK
    if evaluator != None:
        evaluator.tag_count = classifier.label_counts
        evaluator.tag_word_count = classifier.label_feature_count

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
        predicted_tags = [s for s, c in tags_with_score]

        yield tags, tags_with_score

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
