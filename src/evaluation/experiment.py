""" This module runs the experiments to evaluate the
    performance of predicted_results """

import os
import config
import prediction
import kl_distance
import sys
from basket_analysis import *
from log import LOGGER

def to_named_tags(tags, tags_info):
    """ Convert a list of tag ids to text-tags """
    return [tags_info[tag][0] for tag in tags]

# TODO: big problem here
def rerank_tags(scored_tags, get_similarity):
    d = dict(scored_tags)
    # d = dict(zip((k for k, v in scored_tags), (1.0 / math.log(-v)
    #    for k, v in scored_tags)))
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

def run_experiment(predicted_results, settings, limit, predicted_tag_count):
    """ Run the experiment with configuration """
    tags_info = settings["tags_info"]
    sample_count = config.CLASSIFIER["sample_count"]
    # predicted_tag_count = settings["predicted_tag_count"]
    LOGGER.debug("Sample count: %d" % sample_count)
    LOGGER.debug("Max predicted tag count: %d" % predicted_tag_count)

    get_similarity = settings["get_similarity"]

    # run the test
    for index, predict_result in enumerate(predicted_results):
        if index > limit:
            break
        try:
            LOGGER.debug("%d/%d sample" % (index, sample_count))
            orignal, scored_predicted = predict_result
            # TODO: HARD CODED Code again.
            if settings["should_rerank"]:
                scored_predicted = rerank_tags(scored_predicted[:30], get_similarity)
            scored_predicted = scored_predicted[:predicted_tag_count]

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
                LOGGER.debug(log_message)

        except Exception as e:
            LOGGER.error("Error occurs %s" % (str(e)))

    evaluations = []
    for name, evaluator in settings["evaluators"].items():
        evaluation = evaluator.get_evaluation()
        LOGGER.info("%s Precision: %f\t Recall: %f" % (name, evaluation[0], evaluation[1]))
        evaluations.append(evaluation)
    return evaluations


if __name__ == "__main__":
    # Reading the words debug and tags debug from files
    LOGGER.debug("Reading tags and words...")
    tags_info, words_info = prediction.read_tags_and_words()
    LOGGER.debug("Read %d tags and %d words" % (len(tags_info), len(words_info)))

    EXPERIMENT_CONFIG = {
        "classifier": "naive_bayes",
        "evaluator_file": "../../data/stat",
        "predicted_tag_count": [3, 5, 10, 15, 20, 25],
        "tags_info": tags_info,
        "words_info": words_info,
        "should_rerank": False,
        "rounds": 5,
        "sample_count": 10,
        "NAME": "knn.30.new.stat",
        "is_from_classifier": False
    }

    # Generate the classifier
    LOGGER.debug("Creating the naive bayes classifier...")
    classifier = prediction.create_classifier(tags_info, words_info)
    # TODO the following line could be replaced
    # EXPERIMENT_CONFIG["predicted_tags"] = \
    #    prediction.get_sample_results_by_naive_bayes(classifier, tags_info, words_info)

    # Generate the evaluators
    base_path = config.INPUT["base_path"]
    basket_info_file = os.path.join(base_path, "basket.stat")
    train_data_file = os.path.join(base_path, "vectors.stat")

    EXPERIMENT_CONFIG["evaluators"] = {
        "Basket_Evaluator": BasketEvaluator(basket_info_file, train_data_file),
        "KL_Evaluator": kl_distance.KLDistanceEvaluator(classifier.label_counts,
                                                        classifier.label_feature_count,
                                                        "KL_Evaluator.stat")

    }
    EXPERIMENT_CONFIG["get_similarity"] = \
        EXPERIMENT_CONFIG["evaluators"]["Basket_Evaluator"].get_similarity

    group_count = EXPERIMENT_CONFIG["rounds"]

    for predicted_tag_count in EXPERIMENT_CONFIG["predicted_tag_count"]:
        if EXPERIMENT_CONFIG["is_from_classifier"]:
            predict_results = prediction.get_sample_results_by_naive_bayes(
                    classifier, tags_info, words_info)
        else:
            predict_results = prediction.get_predicted_results_from_file(EXPERIMENT_CONFIG["NAME"])
        kl_precision = 0
        kl_recall = 0
        basket_precision = 0
        basket_recall = 0
        print "====================="
        print "Running Test with tag %d"% predicted_tag_count
        sys.stdout.flush()
        for index in xrange(group_count):
            LOGGER.info("\tRun Test %d" % index)
            evaluation = run_experiment(predict_results,
                                        EXPERIMENT_CONFIG,
                                        EXPERIMENT_CONFIG["sample_count"],
                                        predicted_tag_count)
            print "*********************"
            print "Running Test %d" % index
            print "\t\tBasket Precision %f" % evaluation[0][0]
            print "\t\tBasket Recall %f" % evaluation[0][1]
            print "------"
            print "\t\tBasket Precision %f" % evaluation[1][0]
            print "\t\tBasket Recall %f" % evaluation[1][1]
            sys.stdout.flush()
            kl_precision += evaluation[1][0]
            kl_recall += evaluation[1][1]
            basket_precision += evaluation[0][0]
            basket_recall += evaluation[0][1]
        print "\tAverage KL Precision %f" % (kl_precision / group_count)
        print "\tAverage KL Recall %f" % (kl_recall / group_count)
        print "\tAverage basket Precision %f" % (basket_precision / group_count)
        print "\tAverage basket Recall %f" % (basket_recall / group_count)
        sys.stdout.flush()

    # TODO remove the hard coded path
    for name, ev in EXPERIMENT_CONFIG["evaluators"].items():
        ev.save_evaluator("%s.stat" % name)

