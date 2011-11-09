from importor import *
from xml.sax import ContentHandler, parseString, SAXParseException
import config
import db
import os
import post_handler
import sys
import time
import db_access

# -- Statistical information

epoch = time.clock()
def report_progress(i):
    if i == 0:
        return
    if i % 100 == 0:
        print ".",
        sys.stdout.flush()
    if i % 1000 == 0:
        print " -- %d -- %f" % (i, time.clock() - epoch)
        sys.stdout.flush()

# -- Entry
if __name__ == "__main__":
    filename = config.INPUT_FILE["input"]
    error_handler = post_handler.ErrorHandler()
    post_handler = post_handler.PostHandler()

    erase_existing_data = "erase_existing_data" in config.DB and\
                          config.DB["erase_existing_data"]
    db = db.Db(config.DB, erase_existing_data)
    tags = {}
    words = {}

    # TODO: Now we only interested in the vector, not the content
    # post_handler.on_post.append(make_post_importer(db))
    post_handler.on_post.append(make_vector_importer(db,
                         config.INPUT_FILE["stop_words"],
                         tags, words))

    print "pre-processing", time.clock() - epoch
    epoch = time.clock()
    with open(filename) as posts_xml:
        start = config.INPUT_FILE["record_start"]
        count = config.INPUT_FILE["record_count"]
        print ("Range: [%d, %d)"% (start, start + count))

        for i, line in enumerate(posts_xml):
            if i < start:
                continue
            if i >= start + count:
                break

            if i == start:
                print "pre-locate time:", time.clock() - epoch
                start_time = time.clock()
            # TODO: dirty way to filter unwanted tags
            if not line.lstrip().startswith(\
                    "<%s" %
                    config.INPUT_FILE["record_tag"]):
                continue
            parseString(line, post_handler, error_handler)
            report_progress(i)

        print "processing time:", time.clock() - start_time


    # Write the data to the stat file
    db.write_stat_info_back(tags, words)

    stat_dir = config.OUTPUT_FILE["stat_dir"]
    if not os.path.exists(stat_dir):
        os.makedirs(stat_dir)

    db_access.dump_stat(tags,
              os.path.join(stat_dir, "tags.stat"))
    db_access.dump_stat(words,
              os.path.join(stat_dir, "words.stat"))

