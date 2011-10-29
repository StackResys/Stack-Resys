from vectorize import Vectorizor
from xml.sax import ContentHandler, parseString, SAXParseException
import config
import os
import pymongo
import re

def sanitize(content, tag_replaced_by = ""):
    """ Remove the html tags form the content """
    return re.sub("<[^>]*>", tag_replaced_by, content)

def extract_tags(tag_text):
    """ Extract tags """
    return tag_text.strip("><").split("><")

def merge_dict(dict1, dict2):
    """
    WARNING: This methods suppose there's no such a key
    which exists in both dict1 and dict2. If dict1 and
    dict2 has the same key then the value of the specific
    key of dict1 will be overrided by that of the the dict2's
    """
    for key, value in dict2.items():
        dict1[key] = value
    return dict1

class PostEventHandler(ContentHandler):
    def __init__(self, db_config, override=False):
       """
       @param override: erase existing database?
       """
       ContentHandler.__init__(self)
       self.tag = "row"
       self.answer_type = "2"
       self.question_type = "1"
       self.vectorizor = Vectorizor(
        [line[:-1] for line in open(config.INPUT_FILE["stop_words"])])

       # Creating the database connection
       self._connection = pymongo.Connection(
               config.DB["server"],
               config.DB["port"])

       database = db_config["database"]
       collection = db_config["collection"]
       self.questions = \
               self._connection[database][collection["questions"]]
       self.vectors = \
               self._connection[database][collection["vectors"]]
       self.tags = \
               self._connection[database][collection["tags"]]
       self.words = \
               self._connection[database][collection["words"]]

       if override:
           self.questions.remove()

       indexes = db_config["indices"]
       self.questions.create_index(indexes)

    # -- Even Handling
    def startElement(self, name, attributes):
        assert name == self.tag

        if attributes.getValue("PostTypeId") == self.question_type:
            question = self._create_question(attributes)
            self.questions.insert(question)
            vector =  self.vectorizor.vectorize(question["Body"],
                                                question["Tags"])
        elif attributes.getValue("PostTypeId") == self.answer_type:
            answer = self._create_answer(attributes)
            parent_id = answer["ParentId"]
            self.questions.update({"Id": parent_id},
                    {"$push": {"Answers": answer}})
        else:
            assert(False)

    def close():
        self._connection.close()

    # -- Parse the Question
    def _create_post(self, attributes):
        post = {}
        self._add_attr(post, attributes, "Id", int) \
            ._add_attr(post, attributes, "Score", int) \
            ._add_attr(post, attributes, "Body", sanitize) \
            ._add_attr(post, attributes, "OwnerUserId", int)
        return post
    def _create_question(self, attributes):
        question = self._create_post(attributes)
        self._add_attr(question, attributes, "Title") \
            ._add_attr(question, attributes, "Tags", extract_tags) \
            ._add_attr(question, attributes, "FavoriteCount") \
            ._add_attr(question, attributes, "CommentCount") \
            ._add_attr(question, attributes, "AnswerCount")
        return question
    def _create_answer(self, attributes):
        answer = self._create_post(attributes)
        self._add_attr(answer, attributes, "ParentId", int) \
            ._add_attr(answer, attributes, "CommentCount")
        return answer

    def _add_attr(self, question, attributes, key, parse_by = None):
        if not attributes.has_key(key):
            return self

        val = attributes.getValue(key)
        if parse_by is not None:
            val = parse_by(val)
        question[key] = val
        return self

class ErrorHandler:
    def fatalError(self, msg):
        print(msg)

def dump_stat(dic, path):
    sorted_items = sorted(dic.items(), key=lambda v: v[1], reverse = True)
    output = open(path, "w")
    for item in sorted_items:
        output.write("%s: %s\n" % item)

def report_progress(i):
    if i == 0:
        return
    if i % 200 == 0:
        print ".",
    if i % 2000 == 0:
        print " -- %d" % i

if __name__ == "__main__":
    filename = config.INPUT_FILE["input"]
    post_handler = PostEventHandler(config.DB)
    error_handler = ErrorHandler()

    with open(filename) as posts_xml:
        start = config.INPUT_FILE["record_start"]
        end = config.INPUT_FILE["record_end"]
        print ("Range: [%d, %d)"% (start, end))

        for i, line in enumerate(posts_xml):
            if i < start:
                continue
            if i >= end:
                break

            parseString(line, post_handler, ErrorHandler())
            report_progress(i)

    stat_dir = config.INPUT_FILE["stat_dir"]
    if not os.path.exists(stat_dir):
        os.makedirs(stat_dir)

    dump_stat(post_handler.vectorizor.tag_count,
              os.path.join(stat_dir, "tags.stat"))
    dump_stat(post_handler.vectorizor.word_count,
              os.path.join(stat_dir, "words.stat"))

