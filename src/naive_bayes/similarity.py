"""
This module provides several methods the measures
the similarity of two items
"""

import math

def get_kl_distance(counter1, counter2):
    """ Get KL distance of two items
        @param counter1: a key-count dictionary
        @param counter2: a key-count dictionary
        @return the KL distance of counter1 and counter2
    """
    distance = 0

    total_count1 = sum(counter1.values())
    total_count2 = sum(counter2.values())
    for key, count1 in counter1.items():
        if key in counter2:
            count2 = counter2[key]
        else:
            count2 = 0.1

        prob1 = 1.0 * count1 / total_count1
        prob2 = 1.0 * count2 / total_count2
        if prob2 == 0:
            continue

        assert prob1 > 0 and prob1 < 1
        assert prob2 > 0 and prob2 < 1


        distance += (prob1 * (math.log(prob1 / prob2)))
    return distance

def get_translation_probability(label1, label2, counter, reverse_counter):
    """ TODO """
    label_counter = counter[label1]
    label_count = sum(label_counter.values())
    prob = 0.0
    for feature, feature_count in label_counter.items():
        p_feature_label1 = 1.0 * feature_count / label_count


        feature_label_counter = reverse_counter[feature]

        label2_count = 0
        if label2 in feature_label_counter:
            label2_count = feature_label_counter[label2] * 1.0

        p_label2_feature = label2_count / sum(feature_label_counter.values())
        prob += (p_feature_label1 * p_label2_feature)

    return prob



def get_tag_similarity(tag_word_dict, tag1, tag2):
    """ Calcualte the tags similarity based on KL
        Distance """
    if tag1 == tag2:
        return 0
    if tag1 not in tag_word_dict or tag2 not in tag_word_dict:
        return 1

    counter1 = tag_word_dict[tag1]
    counter2 = tag_word_dict[tag2]
    return get_kl_distance(counter1, counter2), \
           get_kl_distance(counter2, counter1)


