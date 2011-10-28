from xml.sax import ContentHandler, parseString, SAXParseException
import re
import pymongo
import config

def sanitize(content, tag_replaced_by = ""):
    """ Remove the html tags form the content """
    return re.sub("<[^>]*>", tag_replaced_by, content)

def extract_tags(tag_text):
    """ Extract tags """
    return tag_text.strip("><").split("><"),

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
    def __init__(self):
       ContentHandler.__init__( self )
       self.tag = "row"
       self.answer_type = "2"
       self.question_type = "1"
       self.post_count = 0

       # Creating the database connection
       self.connection = pymongo.Connection(
               config.DB["server"],
               config.DB["port"])

       database = config.DB["database"]
       collection = config.DB["collection"]
       self.questions = self.connection[database][collection]

       # TODO: this is just used for test
       self.questions.remove()

       indexes = config.DB["indices"]
       self.questions.create_index(indexes)

    def _add_attr(self, question, attributes, key, parse_by = None):
        if not attributes.has_key(key):
            return self

        val = attributes.getValue(key)
        question[key] = val
        return self

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

    # -- Even Handling
    def startElement(self, name, attributes):
        assert name == self.tag

        if attributes.getValue("PostTypeId") == self.question_type:
            question = self._create_question(attributes)
            self.questions.insert(question)
        elif attributes.getValue("PostTypeId") == self.answer_type:
            answer = self._create_answer(attributes)
            parent = answer["ParentId"]
            self.questions.update({"id": parent},
                    {"$push": {"answers": answer}})
        else:
            assert(False)

        self.post_count += 1
        if self.post_count % 100 == 0:
            print(self.post_count)

class ErrorHandler:
    def fatalError(self, msg):
        print(msg)

if __name__ == "__main__":
    filename = config.INPUT_FILE["file_path"]
    post_handler = PostEventHandler()
    error_handler = ErrorHandler()

    with open(filename) as posts_xml:
        for line in posts_xml:
            parseString(line, post_handler, ErrorHandler())
