from re import split
from itertools import groupby


def word_count(word):
    splited = sorted([x for x in split('\s*', word) if x != ''])
    return [(x[0], len(list(x[1]))) for x in groupby(splited)]
