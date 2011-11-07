from xml.sax import ContentHandler, parseString, SAXParseException
import os
import config
import qa_parse

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

if __name__ == "__main__":
    filename = config.INPUT_FILE["input"]
    post_handler = qa_parse.PostEventHandler(config.DB, True)
    error_handler = qa_parse.ErrorHandler()

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

    post_handler.write_stat_info_back()

    stat_dir = config.INPUT_FILE["stat_dir"]
    if not os.path.exists(stat_dir):
        os.makedirs(stat_dir)

    dump_stat(post_handler.tags,
              os.path.join(stat_dir, "tags.stat"))
    dump_stat(post_handler.words,
              os.path.join(stat_dir, "words.stat"))

