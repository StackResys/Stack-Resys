def infinite_list(data):
    while True:
        yield data

def train_translation_distance(source, target):
    # Initialization
    pairs = ((s, t) for s in source for t in target)
    print zip(pairs, infinite_list(0))

train_translation_distance("abcdeft", "123456")

