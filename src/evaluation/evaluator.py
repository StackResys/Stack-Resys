""" This module defines the base class for Evaluator """

class Evaluator:
    """ Evaluator could be used to analyse the precisiona and recall of
    the classified results """
    def __init__(self):
        self.total_recall = 0
        self.total_precision = 0
        self.sample_count = 0

    def update(self, original_tags, predicted_tags):
        """ Invoke update() When new classification results arrives,
            which will update the statistical information. """

        if len(predicted_tags) == 0 or len(original_tags) == 0:
            return 1.0, 1.0

        recalls = {} # recalls for the predicted tags
        precisions = {} # precisions of the predicted tags

        for original in original_tags:
            for predicted in predicted_tags:
                similarity = 1.0 if original == predicted \
                            else self.get_similarity(original, predicted)
                assert similarity >= 0 and similarity <= 1

                _update_with_max_value(recalls, original, similarity)
                _update_with_max_value(precisions, predicted, similarity)

        # Get the recall and precison for this sample
        recall = sum(recalls.values()) * 1.0 / len(predicted_tags)
        precision = sum(precisions.values()) * 1.0 / len(original_tags)

        # Update the global statistical information.
        self.total_recall += recall
        self.total_precision += precision
        self.sample_count += 1

        return precision, recall

    def get_evaluation(self):
        """ Return the recall and precision for all samples """
        return (self.total_precision / self.sample_count,
                self.total_recall / self.sample_count)

    def get_similarity(self, tag1, tag2):
        """ This method is supposed to be override by sub-class"""
        raise RuntimeWarning("Evaluator.get_similarity: This function is not"
                             "Supposed to be invoked")

def _update_with_max_value(dictionary, key, new_value):
    """ A utility function used to make sure the value is maximal """
    dictionary.setdefault(key, 0)
    dictionary[key] = max(dictionary[key], new_value)


