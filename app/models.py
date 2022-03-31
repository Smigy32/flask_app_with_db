from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import base, session


class AuthorModel(base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    books = relationship("BookModel", lazy='dynamic',
                         cascade="all, delete-orphan",
                         foreign_keys="BookModel.author_id")

    @classmethod
    def return_all(cls, offset, limit):
        authors = session.query(cls).order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(author) for author in authors]

    @classmethod
    def find_by_id(cls, author_id, to_dict=True):
        author = session.query(cls).filter_by(id=author_id).first()
        if not author:
            return {}
        if to_dict:
            return cls.to_dict(author)
        else:
            return author

    @classmethod
    def find_by_last_name(cls, last_name, to_dict=True):
        author = session.query(cls).filter_by(last_name=last_name).first()
        if not author:
            return {}
        if to_dict:
            return cls.to_dict(author)
        else:
            return author

    @classmethod
    def delete_by_id(cls, author_id):
        author = session.query(cls).filter_by(id=author_id).first()
        if author:
            session.delete(author)
            session.commit()
            return 200
        else:
            return 404

    def save_to_db(self):
        session.add(self)
        session.commit()

    @staticmethod
    def to_dict(author):
        return {
            "id": author.id,
            "first name": author.first_name,
            "last_name": author.last_name,
            "books": [BookModel.to_dict(b) for b in author.books]
        }


class BookModel(base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    genre = Column(String(30), nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship(AuthorModel, back_populates='books')

    @classmethod
    def return_all(cls, offset, limit):
        books = session.query(cls).order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(book) for book in books]

    @classmethod
    def find_by_id(cls, book_id, to_dict=True):
        book = session.query(cls).filter_by(id=book_id).first()
        if not book:
            return {}
        if to_dict:
            return cls.to_dict(book)
        else:
            return book

    @classmethod
    def find_by_author_id(cls, author_id, offset, limit):
        books = session.query(cls).filter_by(author_id=author_id).order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(book) for book in books]

    @classmethod
    def delete_by_id(cls, book_id):
        book = session.query(cls).filter_by(id=book_id).first()
        if book:
            session.delete(book)
            session.commit()
            return 200
        else:
            return 404

    def save_to_db(self):
        session.add(self)
        session.commit()

    @staticmethod
    def to_dict(book):
        return {
            "id": book.id,
            "title": book.title,
            "genre": book.genre,
            "author_id": book.author_id
        }
