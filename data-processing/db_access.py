import config
import db
import os
import sys

def read_stat_info_from_db(db, tags = {}, words = {},
                           word_filter = {}, tag_filter = {}):
    _read_meta_data(tags, db.tags_table, "tag", tag_filter)
    _read_meta_data(words, db.words_table, "word", word_filter)
    return tags, words

def _read_meta_data(stat, table, key_name, condition={}):
    for info in table.find(condition):
        stat[info[key_name]] = ([info["id"], info["count"]])

def dump_stat(stat, path):
    sorted_items = sorted(stat.items(), key = lambda v: v[1][1], reverse = True)
    output = open(path, "w")
    for item, info in sorted_items:
        output.write("%d:%s:%s\n" % (info[0], item, info[1]))

def dump_vectors(db, path, vector_filter = {}, limit = sys.maxint):
    output = open(path, "w")
    for index, vector in enumerate(db.vectors_table.find(vector_filter)):
        if index % 200 == 0:
            print "."
            sys.stdout.flush()
        merged = _merge_post(vector["posts"])
        tags = vector["tags"]
        _output_vector(merged, tags, output)

def _merge_post(posts):
    result = {}
    for post in posts:
        for w in post:
            result.setdefault(w[0], 0)
            result[w[0]] += w[1]
    return result

def _output_vector(vector, tags, output):
    for k, v in vector.items():
        output.write("%d:%d " % (k, v))
    output.write(";")
    for tag in tags:
        output.write(str(tag))
        output.write(' ')
    output.write("\n")

if __name__ == "__main__":
    tags = {}
    words = {}
    db = db.Db(config.DB, False)

    # -- Read
    out_config = config.OUTPUT_FILE
    # read tags and words
    read_stat_info_from_db(db, tags, words,
                           out_config["word_filter"],
                           out_config["tag_filter"])

    # -- Write
    stat_dir = config.OUTPUT_FILE["stat_dir"]
    dump_vectors(db, os.path.join(stat_dir, "vectors.stat"))

    dump_stat(tags, os.path.join(stat_dir, "tags.stat"))
    dump_stat(words, os.path.join(stat_dir, "words.stat"))

