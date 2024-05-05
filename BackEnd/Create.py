#!/usr/bin/python3
import os
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Enum, ForeignKey, Date
from sqlalchemy.dialects.mysql import VARCHAR, CHAR
from werkzeug.security import generate_password_hash, check_password_hash

# Create the base class using the declarative_base factory function
Base = declarative_base()

# Define the generate_uuid function
def generate_uuid():
    return str(uuid.uuid4())

class Users(Base):
    __tablename__ = "users"
    userID = Column("userID", CHAR(36), primary_key=True, default=generate_uuid)
    FirstName = Column("FirstName", VARCHAR(255))
    LastName = Column("LastName", VARCHAR(255))
    Gender = Column("Gender", Enum("Male", "Female"))
    ProfileName = Column("ProfileName", VARCHAR(255))
    Email = Column("Email", VARCHAR(255))
    PasswordHash = Column("PasswordHash", VARCHAR(128))
    Birthday = Column("Birthday", Date)

    def set_password(self, password):
        self.PasswordHash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.PasswordHash, password)

    def __init__(self, FirstName, LastName, Gender, ProfileName, Email, Password, Birthday):
        self.FirstName = FirstName
        self.LastName = LastName
        self.Gender = Gender
        self.ProfileName = ProfileName
        self.Email = Email
        self.set_password(Password)
        self.Birthday = Birthday

class Posts(Base):
    __tablename__ = "posts"
    PostID = Column("PostID", CHAR(36), primary_key=True, default=generate_uuid)
    UserID = Column("UserID", CHAR(36), ForeignKey('users.userID'))
    PostContent = Column("PostContent", VARCHAR(1024))

    def __init__(self, UserID, PostContent):
        self.UserID = UserID
        self.PostContent = PostContent

class Likes(Base):
    __tablename__ = "likes"
    LikeID = Column("LikeID", CHAR(36), primary_key=True, default=generate_uuid)
    UserID = Column("UserID", CHAR(36), ForeignKey('users.userID'))
    PostID = Column("PostID", CHAR(36), ForeignKey('posts.PostID'))

    def __init__(self, UserID, PostID):
        self.UserID = UserID
        self.PostID = PostID

class Comments(Base):
    __tablename__ = "comments"
    CommentID = Column("CommentID", CHAR(36), primary_key=True, default=generate_uuid)
    UserID = Column("UserID", CHAR(36), ForeignKey('users.userID'))
    PostID = Column("PostID", CHAR(36), ForeignKey('posts.PostID'))
    CommentContent = Column("CommentContent", VARCHAR(1024))

    def __init__(self, UserID, PostID, CommentContent):
        self.UserID = UserID
        self.PostID = PostID
        self.CommentContent = CommentContent

class Follows(Base):
    __tablename__ = "follows"
    FollowID = Column("FollowID", CHAR(36), primary_key=True, default=generate_uuid)
    FollowerID = Column("FollowerID", CHAR(36), ForeignKey('users.userID'))
    FolloweeID = Column("FolloweeID", CHAR(36), ForeignKey('users.userID'))

    def __init__(self, FollowerID, FolloweeID):
        self.FollowerID = FollowerID
        self.FolloweeID = FolloweeID

# Get database credentials from environment variables
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

# Create the database engine
db_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
engine = create_engine(db_url)

# Create all tables known to Base
Base.metadata.create_all(engine)

# Create a new session
Session = sessionmaker(bind=engine)
session = Session()
