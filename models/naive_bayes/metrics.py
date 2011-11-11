import math


# TODO: REFACTOR THIS PART
def calculate_kl_distance(wc1, wc2, wc):
    distance = 0
    total_count1 = sum(wc1.values())
    total_count2 = sum(wc2.values())
    for w, c1 in wc1.items():
        if wc[w] < 100:
            continue
        if w in wc2:
            c2 = wc2[w]
        else:
            c2 = 1

        p1 = 1.0 * c1 / total_count1
        p2 = 1.0 * c2 / total_count2
        if p2 == 0:
            continue

        assert p1 > 0 and p1 < 1
        assert p2 > 0 and p2 < 1


        distance += (p1 * (math.log(p1/p2, 1.4)))
    return distance

def get_tag_similarity(tag_word_dict, wc, tag1, tag2):
    if tag1 == tag2:
        return 0
    if tag1 not in tag_word_dict or tag2 not in tag_word_dict:
        return 1

    wc1 = tag_word_dict[tag1]
    wc2 = tag_word_dict[tag2]
    return calculate_kl_distance(wc1, wc2, wc),\
           calculate_kl_distance(wc2, wc1, wc)

