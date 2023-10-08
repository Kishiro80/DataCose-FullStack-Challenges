# app/models.py

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.config import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)


# Define the association table for the many-to-many relationship between Author and Book
author_book_association = Table(
    "author_book_association",
    Base.metadata,
    Column("author_id", Integer, ForeignKey("authors.id")),
    Column("book_id", Integer, ForeignKey("books.id"))
)


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    # Define the many-to-many relationship between Author and Book
    books = relationship(
        "Book", secondary=author_book_association, back_populates="authors")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    num_pages = Column(Integer)

    # Define the many-to-many relationship between Book and Author
    authors = relationship(
        "Author", secondary=author_book_association, back_populates="books")
