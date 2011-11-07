from xml.sax import ContentHandler, parseString, SAXParseException
import re
import pymongo
import config
from vectorizor import Vectorizor

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
    def __init__(self, db_config, delete_exist_data=True):
       """
       @param override: erase existing database?
       """
       ContentHandler.__init__(self)
       self.tag = "row"
       self.answer_type = "2"
       self.question_type = "1"

       # Creating the database connection
       self._connection = pymongo.Connection(
               config.DB["server"],
               config.DB["port"])

       database = db_config["database"]
       collection = db_config["collection"]
       self._question_table = \
               self._connection[database][collection["questions"]]
       self._vectors_table = \
               self._connection[database][collection["vectors"]]
       self._tags_table = \
               self._connection[database][collection["tags"]]
       self._words_table = \
               self._connection[database][collection["words"]]

       # Reading data from db
       if delete_exist_data:
           self._delete_existing_data()
           self.tags = {}
           self.words = {}
       else:
           self.tags, self.words = self._read_stat_info_from_db()

       indexes = db_config["indices"]
       self._question_table.create_index(indexes)

       stop_words = [line[:-1] for line in
                     open(config.INPUT_FILE["stop_words"])]
       self._vectorizor = Vectorizor(self.tags, self.words, stop_words)

    def write_stat_info_back(self):
        self._write_back(self._tags_table, self.tags, "tag")
        self._write_back(self._words_table, self.words, "word")

    # -- Reading data from MongoDB
    def _delete_existing_data(self):
       self._question_table.remove()
       self._tags_table.remove()
       self._words_table.remove()
       self._vectors_table.remove()

    def _write_back(self, table, info, key_name):
        table.remove
        for key, info in info.items():
            new_item = {
                    key_name: key,
                    "id": info[0],
                    "count": info[1] }
            table.insert(new_item)

    def _read_stat_info_from_db(self):
        return (self._read_meta_data(self._tags_table, "tag"),
                self._read_meta_data(self._words_table, "word"))

    def _read_meta_data(self, table, key_name):
        return dict((info[key_name], [info["id"], info["count"]])
                    for info in table.find())

    # -- Even Handling
    def startElement(self, name, attributes):
        if name != self.tag:
            return

        if attributes.getValue("PostTypeId") == self.question_type:
            question = self._create_question(attributes)
            self._question_table.insert(question)
            vector, tags = \
                self._vectorizor.vectorize(question["Body"],
                                           question["Tags"])
            vector_doc = \
            {
                "id": question["Id"],
                "vector": vector.items(),
                "tags": tags
            }
            self._vectors_table.insert(vector_doc)
        elif attributes.getValue("PostTypeId") == self.answer_type:
            answer = self._create_answer(attributes)
            parent_id = answer["ParentId"]
            self._question_table.update({"Id": parent_id},
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

