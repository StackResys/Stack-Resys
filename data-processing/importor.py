from vectorizor import Vectorizor
import db_access
import time
import sys

def make_vector_importer(db, stop_words_file, all_tags = {}, words = {}):
    db_access.read_stat_info_from_db(db, all_tags, words)
    stop_words = [line[:-1] for line in open(stop_words_file)]
    vectorizor = Vectorizor(all_tags, words, stop_words)

    def _import_vector(post_type, post):
        if post_type == "question":
            vector, tags = vectorizor.vectorize(post["Body"],
                                               post["Tags"])
            vector_doc = \
            {
                "id": post["Id"],
                "posts": [vector.items()],
                "tags": tags
            }
            db.vectors_table.insert(vector_doc)
        else:
            vector, tags = vectorizor.vectorize(post["Body"], {})
            parent_id = post["ParentId"]
            db.vectors_table.update(
                     {"id": parent_id},
                     {"$push": {"posts": vector.items()}})

    return _import_vector

def make_post_importer(db):
    def _import_post(post_type, post):
        if post_type == "question":
            db.question_table.insert(post)
        elif post_type == "answer":
            parent_id = post["ParentId"]
            db.question_table.update({"Id": parent_id},
                    {"$push": {"Answers": post}})
        else:
            assert(False)
    return _import_post

