""" This module is responsible to store/persistent the trained
    naive Bayesian model. """

import naive_bayes

def save_model(classifier, filepath):
    """ Save the trained model to a file """
    output = open(filepath, "w")

    output.write("%d\n" % classifier.total)
    output.write("%f\n" % classifier.beta)
    _save_key_counts(output, classifier.label_counts)
    _save_2_layer_key_counts(
            output, classifier.label_feature_count)

    output.close()

def load_model(filepath):
    """ Load the trained model from a file """
    in_file  = open(filepath)
    classifier = naive_bayes.Classifier()
    classifier.total = int(in_file.readline())
    classifier.beta = float(in_file.readline())
    classifier.label_counts = _load_key_counts(in_file)
    classifier.label_feature_count = \
        _load_2_layer_key_counts(in_file)

    return classifier

# -- Utility
def _save_key_counts(output, key_counts):
    """ Save the dictionary with this structure
            key as string: value as int
    """
    output.write("%d\n" % len(key_counts))
    for key, val in key_counts.items():
        output.write("%s\t%d\n" % (key, val))

def _save_2_layer_key_counts(output, key_counts):
    """ Save the dictionary with this structure
            key as string: value as key_counts
    """
    output.write("%d\n" % len(key_counts))
    for k, key_counts in key_counts.items():
        output.write("%s\n" % k)
        _save_key_counts(output, key_counts)

def _load_key_counts(in_file):
    """ Load the dictionary with this structure
            key as string: value as int
    """
    count = int(in_file.readline())
    key_counts = {}
    for _ in xrange(count):
        parts = in_file.readline()[:-1].split('\t')
        key_counts[int(parts[0])] = int(parts[1])
    return key_counts

def _load_2_layer_key_counts(in_file):
    """ Load the dictionary with this structure
            key as string: value as key_counts
    """
    count = int(in_file.readline())
    key_counts = {}
    for _ in xrange(count):
        k = int(in_file.readline()[:-1])
        key_counts[k] = _load_key_counts(in_file)
    return key_counts

