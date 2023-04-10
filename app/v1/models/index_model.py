from datetime import datetime
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text

class BookIndex(Document):
    title = Text(fields={'keyword': Keyword()})
    author = Text(fields={'keyword': Keyword()})
    summary = Text()
    publisher = Text(fields={'keyword': Keyword()})
    publication_date = Date()
    edition = Integer()

    class Index:
        name = 'book_index'

class MovieIndex(Document):
    title = Text(fields={'keyword': Keyword()})
    director = Text(fields={'keyword': Keyword()})
    summary = Text()
    release_date = Date()
    genre = Keyword()

    class Index:
        name = 'movie_index'

class MusicIndex(Document):
    title = Text(fields={'keyword': Keyword()})
    artist = Text(fields={'keyword': Keyword()})
    album = Text(fields={'keyword': Keyword()})
    release_date = Date()
    genre = Keyword()

    class Index:
        name = 'music_index'
