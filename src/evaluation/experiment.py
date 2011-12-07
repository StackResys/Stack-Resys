""" This module runs the experiments to evaluate the
    performance of predicted_results """

import os
import config
import prediction
import kl_distance
from basket_analysis import *
from log import LOGGER
import math

def to_named_tags(tags, tags_info):
    """ Convert a list of tag ids to text-tags """
    return [tags_info[tag][0] for tag in tags]

def enhance_tags(scored_tags, get_similarity):
    # TODO dirty code
    d = dict(zip((k for k, v in scored_tags), (1.0 / math.log(-v)
        for k, v in scored_tags)))
    for tag, score in scored_tags:
        other_tags = (other_tag for other_tag, score in scored_tags if tag != other_tag)
        for other in other_tags:
            similarity = get_similarity(tag, other)
            if similarity == 0:
                continue
            d[other] += (score * similarity)
    scored_tags = d.items()
    scored_tags.sort(key = lambda x: x[1])
    return scored_tags

def run_experiment(settings):
    """ Run the experiment with configuration """
    tags_info = settings["tags_info"]
    sample_count = config.CLASSIFIER["sample_count"]
    predicted_tag_count = settings["predicted_tag_count"]
    LOGGER.info("Sample count: %d" % sample_count)
    LOGGER.info("Max predicted tag count: %d" % predicted_tag_count)

    predict_results = settings["predicted_tags"]
    get_similarity = settings["get_similarity"]

    # run the test
    for index, predict_result in enumerate(predict_results):
        if index > sample_count:
            break

        LOGGER.info("%d/%d sample" % (index, sample_count))
        try:
            orignal, scored_predicted = predict_result
            scored_predicted = enhance_tags(scored_predicted[:30], get_similarity)[:10]
            # scored_predicted = scored_predicted[:10]

            predicted = [t for t, s in scored_predicted]

            # TODO: SOME PROBLEM may raise here
            predicted = predicted[:predicted_tag_count]

            for name, evaluator in settings["evaluators"].items():
                evaluation = evaluator.update(orignal, predicted)
                log_message = "\nOriginal Result: %s\n"\
                              "Predicted Result: %s\n"\
                              "Evaluator Type: %s\n"\
                              "\tPrecision: %f\n"\
                              "\tRecall: %f\n" % (
                                    str(to_named_tags(orignal, tags_info)),
                                    str(to_named_tags(predicted, tags_info)),
                                    name, evaluation[0], evaluation[1])
                LOGGER.info(log_message)

        except Exception as e:
            LOGGER.error("Error occurs %s" % (str(e)))

    for name, evaluator in settings["evaluators"].items():
        evaluation = evaluator.get_evaluation()
        LOGGER.info("%s Precision: %f\t Recall: %f" % (name, evaluation[0], evaluation[1]))


if __name__ == "__main__":
    # Reading the words info and tags info from files
    LOGGER.info("Reading tags and words...")
    tags_info, words_info = prediction.read_tags_and_words()
    LOGGER.info("Read %d tags and %d words" % (len(tags_info), len(words_info)))

    EXPERIMENT_CONFIG = {
        "classifier": "naive_bayes",
        "evaluator_file": "../../data/stat",
        "predicted_tag_count": 30,
        "tags_info": tags_info,
        "words_info": words_info,
    }

    # Generate the classifier
    LOGGER.info("Creating the naive bayes classifier...")
    classifier = prediction.create_classifier(tags_info, words_info)
    # TODO the following line could be replaced
    EXPERIMENT_CONFIG["predicted_tags"] = \
        prediction.get_sample_results_by_naive_bayes(classifier, tags_info, words_info)

    # Generate the evaluators
    base_path = config.INPUT["base_path"]
    basket_info_file = os.path.join(base_path, "basket.stat")
    train_data_file = os.path.join(base_path, "vectors.stat")

    EXPERIMENT_CONFIG["evaluators"] = {
        "Basket Evaluator": BasketEvaluator(basket_info_file, train_data_file),
        "KL Evaluator": kl_distance.KLDistanceEvaluator(classifier.label_counts,
                                                        classifier.label_feature_count,
                                                        "")
    }
    EXPERIMENT_CONFIG["get_similarity"] = \
        EXPERIMENT_CONFIG["evaluators"]["Basket Evaluator"].get_similarity


    run_experiment(EXPERIMENT_CONFIG)
