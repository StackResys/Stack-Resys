""" This module runs the experiments to evaluate the
    performance of predicted_results """

import sys
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

def enhance_tags(scored_tags, basket_evaluator):
    d = dict(zip((k for k, v in scored_tags), (1.0 / math.log(-v) for k, v in scored_tags)))
    for tag, score in scored_tags:
        other_tags = (other_tag for other_tag, score in scored_tags if tag != other_tag)
        for other in other_tags:
            similarity = basket_evaluator.get_similarity(tag, other)
            if similarity == 0:
                continue
            d[other] += (score * similarity)
    scored_tags = d.items()
    scored_tags.sort(key = lambda x: x[1])
    return scored_tags

def run_experiment(experiment_settings):
    """ Run the experiment with configuration """
    # Reading the words info and tags info from files
    LOGGER.info("Reading tags and words...")
    tags_info, words_info = prediction.read_tags_and_words()
    LOGGER.info("Read %d tags and %d words" % (len(tags_info), len(words_info)))

    sample_count = config.CLASSIFIER["sample_count"]
    predicted_tag_count = experiment_settings["predicted_tag_count"]
    LOGGER.info("Sample count: %d" % sample_count)
    LOGGER.info("Max predicted tag count: %d" % predicted_tag_count)

    # Generate the evaluators
    base_path = config.INPUT["base_path"]
    basket_info_file = os.path.join(base_path, "basket.stat")
    train_data_file = os.path.join(base_path, "vectors.stat")
    evaluator2 = BasketEvaluator(basket_info_file, train_data_file)

    # TODO: DIRTY HACK

    evaluator1 =\
        kl_distance.KLDistanceEvaluator(None, None, experiment_settings["evaluator_file"])
    predict_results = prediction.get_sample_results_by_naive_bayes(tags_info, words_info, evaluator1)

    """
    for hack in predict_results:
        break
    predict_results = prediction.get_predicted_results_from_file("../../data/test_results/knn.txt")
    """
    # run the test
    for index, predict_result in enumerate(predict_results):
        if index > sample_count:
            break

        LOGGER.info("%d/%d sample" % (index, sample_count))
        try:
            orignal, scored_predicted = predict_result
            scored_predicted = enhance_tags(scored_predicted[:30], evaluator2)[:10]
            # scored_predicted = scored_predicted[:10]

            predicted = [t for t, s in scored_predicted]

            # TODO: SOME PROBLEM may raise here
            predicted = predicted[:predicted_tag_count]

            evaluation1 = evaluator1.update(orignal, predicted)
            evaluation2 = evaluator2.update(orignal, predicted)
            log_message = "\nOriginal Result: %s\n"\
                          "Predicted Result: %s\n"\
                          "Evaluation 1: P: %f, R: %f\n"\
                          "Evaluation 2: P: %f, R: %f\n" % (
                                str(to_named_tags(orignal, tags_info)),
                                str(to_named_tags(predicted, tags_info)),
                                evaluation1[0], evaluation1[1],
                                evaluation2[0], evaluation2[1])
            LOGGER.info(log_message)
        except Exception as e:
            LOGGER.error("Error occurs %s" % (str(e)))
    LOGGER.info("KL Distance Evaluation P & R: %s" % str(evaluator1.get_evaluation()))
    LOGGER.info("Basket Evaluation P & R: %s" % str(evaluator2.get_evaluation()))


if __name__ == "__main__":
    EXPERIMENT_CONFIG = {
        "classifier": "naive_bayes",
        "evaluator_file": "../../data/stat",
        "predicted_tag_count": 30
    }

    run_experiment(EXPERIMENT_CONFIG)
