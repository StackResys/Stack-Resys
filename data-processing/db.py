import pymongo

class Db:
    def __init__(self, db_config, delete_exist_data):
       self.connection = pymongo.Connection(
               db_config["server"],
               db_config["port"])

       database = db_config["database"]
       collection = db_config["collection"]
       self.question_table = \
               self.connection[database][collection["questions"]]
       self.vectors_table = \
               self.connection[database][collection["vectors"]]
       self.tags_table = \
               self.connection[database][collection["tags"]]
       self.words_table = \
               self.connection[database][collection["words"]]

       # delete all data if required
       if delete_exist_data:
           self._delete_existing_data()

       # Creating the index
       indexes = db_config["indices"]
       self.question_table.create_index(indexes)

    def _delete_existing_data(self):
       self.question_table.remove()
       self.tags_table.remove()
       self.words_table.remove()
       self.vectors_table.remove()
