from xml.sax import ContentHandler, parseString, SAXParseException
import os
import config
import post_handler
import db
from importor import *

# -- Statistical information
def dump_stat(dic, path):
    sorted_items = sorted(dic.items(), key=lambda v: v[1][1], reverse = True)
    output = open(path, "w")
    for item, info in sorted_items:
        output.write("%s: %s\n" % (item, info[1]))

def report_progress(i):
    if i == 0:
        return
    if i % 200 == 0:
        print ".",
    if i % 2000 == 0:
        print " -- %d" % i

# -- Data Persistence

# -- Entry
if __name__ == "__main__":
    filename = config.INPUT_FILE["input"]
    error_handler = post_handler.ErrorHandler()
    post_handler = post_handler.PostHandler()

    db = db.Db(config.DB, False)
    tags = {}
    words = {}

    # TODO: Now we only interested in the vector, not the content
    # post_handler.on_post.append(make_post_importer(db))
    post_handler.on_post.append(make_vector_importer(db,
                         config.INPUT_FILE["stop_words"],
                         tags, words))

    with open(filename) as posts_xml:
        start = config.INPUT_FILE["record_start"]
        end = config.INPUT_FILE["record_end"]
        print ("Range: [%d, %d)"% (start, end))

        for i, line in enumerate(posts_xml):
            if i < start:
                continue
            if i >= end:
                break

            # TODO: dirty way to filter unwanted tags
            if not line.lstrip().startswith(\
                    "<%s" %
                    config.INPUT_FILE["record_tag"]):
                continue
            parseString(line, post_handler, error_handler)
            report_progress(i)


    # Write the data to the stat file
    db.write_stat_info_back(tags, words)

    stat_dir = config.INPUT_FILE["stat_dir"]
    if not os.path.exists(stat_dir):
        os.makedirs(stat_dir)

    dump_stat(tags,
              os.path.join(stat_dir, "tags.stat"))
    dump_stat(words,
              os.path.join(stat_dir, "words.stat"))

