from elasticsearch_dsl import Document, Keyword, Text, DenseVector


class IndexBase(Document):
    uid = Text()
    title = Text()
    details = Text()
    embeddings = DenseVector()
    posted = Text()
    tags = Keyword()
    link = Text()

class HouzzIndex(IndexBase):
    author = Keyword()
    description = Text()
    related_tags = Keyword()
    
    class Index:
        name = 'houzz'

class CnnIndex(IndexBase):
    channel = Keyword()
    comment_count = Text()
    likes = Text()
    views = Text()
    
    class Index:
        name = 'cnn'

class TedtalkIndex(IndexBase):
    author = Keyword()
    views = Text()
    
    class Index:
        name = 'tedtalk'


