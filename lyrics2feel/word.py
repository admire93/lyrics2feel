from re import split
from itertools import groupby

from sqlalchemy.types import Integer, Unicode
from sqlalchemy.schema import Column

from .db import Base


class Word(Base):

    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)

    word = Column(Unicode, nullable=False)

    score = Column(Integer)


def word_count(word):
    splited = sorted([x for x in split('\s*', word) if x != ''])
    return [(x[0], len(list(x[1]))) for x in groupby(splited)]
