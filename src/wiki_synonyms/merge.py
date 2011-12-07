""" TODO: ADD DOC STRING """

import sys

def parseline(line, sep):
    """ TODO: ADD DOC STRING """
    # TODO: the '\t' shouldn't be hard coded here.
    # TODO: Also remember to refactor the "key" logic, it is not
    # necessarily to be the 0-th

    # line == "" means the file has reached the end of the file
    if line == "":
        return None
    record = line[:-1].split(sep)
    return {"key": int(record[0]), "rest": record[1:]}

def merge(input1, input2, sep):
    """ TODO: ADD DOC STRING """
    # TODO: what is the key that are used for join

    # TODO: how to deal with such kind duplication
    record1 = parseline(input1.readline(), sep)
    record2 = parseline(input2.readline(), sep)

    while record1 is not None and record2 is not None:
        if record1["key"] == record2["key"]:
            print "%s\t%s\t%s" % (record1["key"], \
                                  sep.join(record1["rest"]),
                                  sep.join(record2["rest"]))
            record1 = parseline(input1.readline(), sep)
            record2 = parseline(input2.readline(), sep)
        elif record1["key"] < record2["key"]:
            record1 = parseline(input1.readline(), sep)
        else:
            record2 = parseline(input2.readline(), sep)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Expect 2 files, but only %d file provided" %
                         (len(sys.argv) - 1))
        sys.exit(1)
    merge(open(sys.argv[1]), open(sys.argv[2]), '\t')

