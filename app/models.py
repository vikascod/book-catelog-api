from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Date
from app.database import Base
from datetime import datetime, date
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_on = Column(DateTime, default=datetime.utcnow)

    reviews = relationship("Review", back_populates="user")
    books = relationship("Book", back_populates="user")

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), unique=True, nullable=False)
    author = Column(String(200), nullable=False)
    description = Column(String(300), nullable=True)
    price = Column(Integer, default=0)
    publisher = Column(String(200), nullable=False)
    language = Column(String(200), nullable=False)
    genre = Column(String(200), nullable=False)
    book_image = Column(String(300), nullable=False)
    in_stock = Column(Boolean, default=False)
    published_date = Column(Date, default=date.today)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="books")
    reviews = relationship("Review", back_populates="book")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    text = Column(String)
    rating = Column(Integer)

    book = relationship("Book", back_populates="reviews")
    user = relationship("User", back_populates="reviews")


