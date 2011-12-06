""" BasketEvaluator analyses co-occurrences to get the similarity """
import evaluator
import pickle
import os
from log import LOGGER

def analyse_baskets(baskets):
    """ This function analyse the co-occurrance of baskets """
    item_counts = {}
    item_cooccurrence = {}
    total_count = 0
    for basket in baskets:
        total_count += 1

        # Update the item count
        for item in basket:
            item_counts.setdefault(item, 0)
            item_counts[item] += 1

        # Update the co-occurrence
        pairs = ((item1, item2)
                 for item1 in basket for item2 in basket
                 if item1 < item2)
        for pair in pairs:
            item_cooccurrence.setdefault(pair, 0)
            item_cooccurrence[pair] += 1

    return (item_counts, item_cooccurrence, total_count)

def _create_baskets(basket_info_file):
    """ Create a generator of baskets from a specific file """
    for line in open(basket_info_file):
        tags = [int(tag) for tag in line[:-1].split(';')[2].split()]
        yield tags

class BasketEvaluator(evaluator.Evaluator):
    """ Evaluator that used the associative analysis
        to calculate the similarity """
    def __init__(self, basket_info_file = "",
                 train_data_file = "", support = 10):
        """ ***Note***: If both basket_info_file and train_data_file
                        exist, ignore the "train_data_file". """
        evaluator.Evaluator.__init__(self)

        # -- Create basket info from test data
        if not os.path.exists(basket_info_file):
            LOGGER.info("Basket info file %s not found" % basket_info_file)
            LOGGER.info("Get basket form training data...")
            baskets = _create_baskets(train_data_file)
            tags_info = analyse_baskets(baskets)
            LOGGER.info(
                "Writing back the basket info to " + basket_info_file)
            # Save the tags info to the disk
            pickle.dump(tags_info, open(basket_info_file, "wb"))
        else:
            LOGGER.info("basket info file %s found" % basket_info_file)
            LOGGER.info("Loading the basket_info_file ...")
            # Read the tag info from the file
            tags_info = pickle.load(open(basket_info_file, "rb"))
            LOGGER.info("Basket info read!")

        self.tag_counts, self.cooccurrences, self.total_count = tags_info
        self.support = support

    def get_similarity(self, tag1, tag2):
        """ Get the similarity by the co-occurrence """
        if tag1 == tag2:
            return 1.0
        key = (tag1, tag2) if tag1 < tag2 else (tag2, tag1)

        if key not in self.cooccurrences:
            return 0.0

        occurrence = self.cooccurrences[key]
        if occurrence < self.support:
            return 0.0

        assert tag2 in self.tag_counts and self.tag_counts[tag2] > 0
        return 1.0 * occurrence / self.tag_counts[tag1]



