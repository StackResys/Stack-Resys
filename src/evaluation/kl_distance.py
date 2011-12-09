""" This modules provides methods and classes related to K-L distance """

import math
import evaluator
import pickle
import os

def get_kl_distance(counts1, counts2):
    """ Get KL distance of two items
        @param counts1: a key-count dictionary
        @param counts2: a key-count dictionary
        @return the KL distance of counts1 and counts2
    """
    distance = 0

    total_count1 = sum(counts1.values())
    total_count2 = sum(counts2.values())
    for key, count2 in counts2.items():
        if key in counts1:
            count1 = counts1[key]
        else:
            count1 = 0.1

        prob1 = 1.0 * count1 / total_count1
        prob2 = 1.0 * count2 / total_count2
        if prob1 == 0:
            continue

        assert prob1 > 0 and prob1 < 1
        assert prob2 > 0 and prob2 < 1

        distance += (prob2 * (math.log(prob2 / prob1)))
    return distance

def get_tag_similarity(tag_word_dict, tag1, tag2):
    """ Calcualte the tags similarity based on KL
        Distance """
    if tag1 == tag2:
        return 1.0
    if tag1 not in tag_word_dict or tag2 not in tag_word_dict:
        return 0.0

    counts1 = tag_word_dict[tag1]
    counts2 = tag_word_dict[tag2]
    distance = get_kl_distance(counts1, counts2)

    score = normalize_distance(distance)
    return score

def normalize_distance(distance):
    """ normalize the distance to similarity,
        which is in the range of [0, 1] """
    return 1 / math.e ** ((distance ** 1.5) * 3)

class KLDistanceEvaluator(evaluator.Evaluator):
    """ This evauator use KL-distance to evaluate the similarity """
    def __init__(self, tag_count, tag_word_count, saved_file = ""):
        evaluator.Evaluator.__init__(self)
        self.tag_count = tag_count
        self.tag_word_count = tag_word_count

        self.similarities = {}
        self.saved_file = saved_file
        if saved_file != "" and os.path.exists(saved_file):
            self.similarities = pickle.load(open(saved_file, "rb"))
    def save_evaluator(self, saved_file):
        pickle.dump(self.similarities, open(saved_file, "wb"))

    def get_similarity(self, tag1, tag2):
        key = (tag1, tag2)
        if key not in self.similarities:
            self.similarities[key] = get_tag_similarity(self.tag_word_count, tag1, tag2)
        return self.similarities[key]
