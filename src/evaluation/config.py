import sys
sys.path.append("../naive_bayes/")
from kl_distance import KLDistanceEvaluator
import logging

INPUT = {
    "word_threshold": 10,
    "tag_threshold": 5,
    "base_path": "../../data/stat/",
}

EXPERIMENT = {
    "predicted_tag_count": 30
}

PIPELINES = {
    "default": {
        "evaluator": KLDistanceEvaluator,
        "classifier": "naive_bayes",
        "evaluator_file": "../../data/stat"
    }
}

BAYES_CLASSIFIER = {
    "retrain_model": False,
    "beta" : 0.5,
    "train_count": 300000,
    "sample_count": 5000,
}

CLASSIFIER = {
    "retrain_model": False,
    "beta" : 0.5,
    "train_count": 300000,
    "sample_count": 5000
}