from xml.sax import ContentHandler, parseString, SAXParseException
import re

class PostHandler(ContentHandler):
    # -- Initialization
    def __init__(self):
       """
       @param override: erase existing database?
       """
       ContentHandler.__init__(self)
       self.tag = "row"
       self.answer_type = "2"
       self.question_type = "1"
       self.on_post = []

    # -- Even Handling
    def startElement(self, name, attributes):
        if name != self.tag:
            return

        if attributes.getValue("PostTypeId") == self.question_type:
            question = self._create_question(attributes)
            self._on_post("question", question)
        elif attributes.getValue("PostTypeId") == self.answer_type:
            answer = self._create_answer(attributes)
            self._on_post("answer", answer)
        else:
            assert(False)

    def close():
        self.connection.close()

    def _on_post(self, post_type, post):
        for listener in self.on_post:
            listener(post_type, post)

    # -- Parse the Question
    def _create_post(self, attributes):
        post = {}
        self._add_attr(post, attributes, "Id", int) \
            ._add_attr(post, attributes, "Score", int) \
            ._add_attr(post, attributes, "Body", _sanitize) \
            ._add_attr(post, attributes, "OwnerUserId", int)
        return post
    def _create_question(self, attributes):
        question = self._create_post(attributes)
        self._add_attr(question, attributes, "Title") \
            ._add_attr(question, attributes, "Tags", _extract_tags) \
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

# -- Utilities
def _sanitize(content, tag_replaced_by = ""):
    """ Remove the html tags form the content """
    return re.sub("<[^>]*>", tag_replaced_by, content)

def _extract_tags(tag_text):
    """ Extract tags """
    return tag_text.strip("><").split("><")

def _merge_dict(dict1, dict2):
    """
    WARNING: This methods suppose there's no such a key
    which exists in both dict1 and dict2. If dict1 and
    dict2 has the same key then the value of the specific
    key of dict1 will be overrided by that of the the dict2's
    """
    for key, value in dict2.items():
        dict1[key] = value
    return dict1

