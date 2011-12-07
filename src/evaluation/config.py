import sys
sys.path.append("../naive_bayes/")
from kl_distance import KLDistanceEvaluator

INPUT = {
    "word_threshold": 10,
    "tag_threshold": 5,
    "base_path": "../../data/stat/",
}

CLASSIFIER = {
    "retrain_model": False,
    "beta" : 0.5,
    "train_count": 300000,
    "sample_count": 5000
}
