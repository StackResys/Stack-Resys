import bayesianClassifier

def save(classifier, filepath):
    output = open(filepath, "w")

    output.write("%d\n" % classifier.total)
    output.write("%f\n" % classifier.beta)
    _save_dict(output, classifier.labelCount)
    _save_2_layer_dict(output, classifier.labelFeatureCount)

    output.close()

def load(filepath):
    input  = open(filepath)
    classifier = bayesianClassifier.BayesianClassifier()
    classifier.total = int(input.readline())
    classifier.beta = float(input.readline())
    classifier.labelCount = _load_dict(input)
    classifier.labelFeatureCount = _load_2_layer_dict(input)

    return classifier

def _save_dict(output, d):
    output.write("%d\n" % len(d))
    for k, v in d.items():
        # TODO: the following bug, surprisingly, can yield a rather
        # good performance in calculating tag similarity. Will figure
        # out later.
        # output.write("%s\t%d\n" % (k, len(v)))
        output.write("%s\t%d\n" % (k, v))

def _save_2_layer_dict(output, d):
    output.write("%d\n" % len(d))
    for k, d in d.items():
        output.write("%s\n" % k)
        _save_dict(output, d)

def _load_dict(input):
    count = int(input.readline())
    d = {}
    for i in xrange(count):
        parts = input.readline()[:-1].split('\t')
        d[int(parts[0])] = int(parts[1])
    return d

def _load_2_layer_dict(input):
    count = int(input.readline())
    d = {}
    for i in xrange(count):
        k = int(input.readline()[:-1])
        d[k] = _load_dict(input)
    return d

