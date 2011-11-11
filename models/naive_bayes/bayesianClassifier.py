import math

class BayesianClassifier:
    def __init__(self, beta = 0):
        # total occurrence of all features
        self.total = 0
        # Labels and their occurrence
        self.labelCount = {}
        # Features' occurrence under certain label
        self.labelFeatureCount = {}
        # beta value
        self.beta = beta

    def train(self, features, labels):
        # Update the counting of the attributes under differnt labels
        for label in labels:
            for feature, count in features.items():
                self.total += count
                label_wc = self.labelFeatureCount.setdefault(label, {})
                label_wc.setdefault(feature, 0)
                label_wc[feature] += count

                self._updateCount(self.labelCount, label, count)

    def classify(self, features):
        scores = sorted(((label, self.getScore(features, label)) for \
                        label in self.labelCount.keys()), \
                        key = lambda x: x[1], \
                        reverse = True)

        scores = self._normalize_score(scores)
        return scores

    def getScore(self, features, label):
        totalScore = self._getScoreOfOneFeature(self.labelCount[label], self.total)
        fc = len(self.labelCount)
        lCount = self.labelCount[label]

        for feature, count in features.items():
                key = (label, feature)
                fCount = 0
                if label in self.labelFeatureCount and \
                   feature in self.labelFeatureCount[label]:
                    fCount =self.labelFeatureCount[label][feature]

                score = self._getScoreOfOneFeature(fCount + self.beta, lCount + fc * self.beta)
                totalScore += count * score
        return totalScore

    def _updateCount(self, d, key, val = 1):
        d.setdefault(key, 0)
        d[key] += val

    def _getScoreOfOneFeature(self, n1, n2):
        if n1 == 0:
            return 0
        return math.log(n1 * 1.0 / n2, 2)

    def _normalize_score(self, scores):
        total = sum(s for k, s in scores)
        scores = [(k, math.log(1 - s/total)) for k, s in scores]
        return scores


if __name__ == "__main__":
    def split(text):
        return dict((token, 1) for token in text.split())
    classifier = BayesianClassifier(0.5)
    classifier.train(split("money money is making finance"), ["finance"])
    classifier.train(split("Best coffee shop in Pit? I enjoy days with friends! life is here"), ["life", "pit"])
    classifier.train(split("life life life good"), ["life"])
    classifier.train(split("money doesn't make friend with don't give up life, you"), ["finance", "life"])

    print classifier.classify(split("money wall is finance"))
    print classifier.classify(split("life is good"))



