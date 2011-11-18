from db_access import *

if __name__ == "__main__":
    tags = {}
    words = {}
    db = db.Db(config.DB, False)

    # -- Read
    out_config = config.OUTPUT_FILE
    # read tags and words
    read_stat_info_from_db(db, tags, words,
                           out_config["word_filter"],
                           out_config["tag_filter"])

    # -- Write
    stat_dir = config.OUTPUT_FILE["stat_dir"]
    dump_vectors(db, os.path.join(stat_dir, "vectors.stat"))

    dump_stat(tags, os.path.join(stat_dir, "tags.stat"))
    dump_stat(words, os.path.join(stat_dir, "words.stat"))

