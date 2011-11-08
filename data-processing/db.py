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
       for collection, index in indexes.items():
           print collection, index
           print self.connection[database][collection]
           self.connection[database][collection].create_index(index)

    # -- Write back data
    def write_stat_info_back(self, tags, words):
        self._write_back(self.tags_table, tags, "tag")
        self._write_back(self.words_table, words, "word")

    # -- Reading data from MongoDB
    def _write_back(self, table, info, key_name):
       table.remove()
       for key, info in info.items():
           new_item = {
                   key_name: key,
                   "id": info[0],
                   "count": info[1] }
           table.insert(new_item)

    def _delete_existing_data(self):
       self.question_table.remove()
       self.tags_table.remove()
       self.words_table.remove()
       self.vectors_table.remove()

