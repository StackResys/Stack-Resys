""" module for Naive Bayesian Classifier """
import math

class Classifier:
    """ Classifier the classifier based on Naive Theorm """
    def __init__(self, beta = 0):
        # total occurrence of all features
        self.total = 0
        # Labels and their occurrence
        self.label_counts = {}
        # Features' occurrence under certain label
        self.label_feature_count = {}
        # beta value
        self.beta = beta

    def train(self, features, labels):
        """ Training the classifier
            @param features: list of features of training data
            @param labels: list of labels. training data could have one or
                           more labels
        """
        # Update the counting of the attributes under differnt labels
        for label in labels:
            for feature, count in features.items():
                self.total += count
                label_wc = self.label_feature_count.setdefault(label, {})
                label_wc.setdefault(feature, 0)
                label_wc[feature] += count

                _update_count(self.label_counts, label, count)

    def classify(self, features):
        """ Classify item according to its features
            @param: features: list of features of the item
            @return: return the scores of the labels, sorted by the scores.
        """
        scores = sorted(((label, self.get_score(features, label)) for \
                        label in self.label_counts.keys()), \
                        key = lambda x: x[1], \
                        reverse = True)

        return scores

    def get_score(self, features, label):
        """ Get the likelihood of a list of features being
            categoried to a specific label """
        label_count = self.label_counts[label]
        unique_label_count = len(self.label_counts)
        label_score = _get_log_fraction(self.label_counts[label],
                                        self.total)

        total_score = label_score
        for feature, count in features.items():
            feature_count = 0

            # Update the feature_count if both feature
            # and label have been seen before
            is_label_exist = label in self.label_feature_count
            is_feature_exist = feature in self.label_feature_count[label]
            if is_label_exist and is_feature_exist:
                feature_count = self.label_feature_count[label][feature]

            score = _get_log_fraction(
                        feature_count + self.beta,
                        label_count + unique_label_count * self.beta)
            total_score += count * score
        return total_score

# -- Utilities
def _update_count(count_dict, key, val = 1):
    """ safely update the "count dictionary" """
    count_dict.setdefault(key, 0)
    count_dict[key] += val

def _get_log_fraction(part_count, total_count):
    """ apply the log function to fraction so that we can
        convert it into bigger number, which will greatly
        ease the processing """
    if part_count == 0:
        return 0
    return math.log(part_count * 1.0 / total_count, 2)

def _split(text):
    """ Used for test only """
    return dict((token, 1) for token in text.split())

if __name__ == "__main__":
    PREDICTOR = Classifier(0.5)
    PREDICTOR.train(_split("money money is making finance"), ["finance"])
    PREDICTOR.train(
        _split("Best coffee shop in Pit?"
              "I enjoy days with friends! life is here"),
        ["life", "pit"])
    PREDICTOR.train(_split("life life life good"), ["life"])
    PREDICTOR.train(_split("money doesn't make friend "
                           "with don't give up life, you"),
                     ["finance", "life"])

    print PREDICTOR.classify(_split("money wall is finance"))
    print PREDICTOR.classify(_split("life is good"))

