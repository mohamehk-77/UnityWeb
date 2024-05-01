#!/usr/bin/python3
import os
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Enum, ForeignKey, Date
from sqlalchemy.dialects.mysql import VARCHAR, CHAR
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

# Create the base class using the declarative_base factory function
Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())


class Users(Base):
    __tablename__ = "users"
    userID = Column("userID", CHAR(36), primary_key=True,
                    default=generate_uuid)
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
    UserID = Column("UserID", CHAR(36), ForeignKey('users.userID'))  # Corrected
    PostContent = Column("PostContent", VARCHAR(1024))

    def __init__(self, UserID, PostContent):
        self.UserID = UserID
        self.PostContent = PostContent


class Likes(Base):
    __tablename__ = "likes"
    LikeID = Column("LikeID", CHAR(36), primary_key=True,
                    default=generate_uuid)
    UserID = Column("UserID", CHAR(36), ForeignKey('users.userID'))
    PostID = Column("PostID", CHAR(36), ForeignKey('posts.PostID'))

    def __init__(self, UserID, PostID):
        self.UserID = UserID
        self.PostID = PostID


def generate_uuid():
    return str(uuid.uuid4())


class Comments(Base):
    __tablename__ = "comments"
    CommentID = Column("CommentID", CHAR(36), primary_key=True,
                       default=generate_uuid)
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


def add_user(FirstName, LastName, Gender, ProfileName, Email, Password, Birthday):
    Email_exist = session.query(Users).filter(Users.Email == Email).all()
    Profile_Name_Exist = session.query(Users).filter(Users.ProfileName == ProfileName).all()
    if len(Email_exist) > 0:
        print("Email Address already exists")
    elif len(Profile_Name_Exist) > 0:
        print("That ProfileName Was Taken Please Chose Another One!")
    else:
        user = Users(FirstName=FirstName, LastName=LastName, Gender=Gender, ProfileName=ProfileName, Email=Email, Password=Password, Birthday=Birthday)
        session.add(user)
        session.commit()


def add_post(UserID, PostContent):
    post = Posts(UserID=UserID, PostContent=PostContent)
    session.add(post)
    session.commit()
    print("Post Added")


def add_or_remove_like(UserID, PostID):
    existing_like = session.query(Likes).filter_by(UserID=UserID, PostID=PostID).first()
    if existing_like:
        session.delete(existing_like)
        session.commit()
        print("Like removed")
    else:
        like = Likes(UserID=UserID, PostID=PostID)
        session.add(like)
        session.commit()
        print("Like added")


def add_comment(UserID, PostID, CommentContent):
    comment = Comments(UserID=UserID, PostID=PostID, CommentContent=CommentContent)
    session.add(comment)
    session.commit()


def add_follow(FollowerID, FolloweeID):
    existing_follow = session.query(Follows).filter_by(FollowerID=FollowerID, FolloweeID=FolloweeID).first()
    if existing_follow:
        session.delete(existing_follow)
        session.commit()
        print("Unfollowed")
        return jsonify({"message": "Unfollowed"}), 200
    else:
        follow = Follows(FollowerID=FollowerID, FolloweeID=FolloweeID)
        session.add(follow)
        session.commit()
        print("Followed")
        return jsonify({"message": "Followed"}), 200


def is_authorized_to_edit_post(userID, postID):
    post = session.query(Posts).filter_by(UserID=userID, PostID=postID).first()
    if post and post.UserID == userID:
        return True
    return False


def edit_post(PostID, new_content):
    post = session.query(Posts).filter_by(PostID=PostID).first()
    if post:
        post.PostContent = new_content
        session.commit()
        print("Post updated")
    else:
        print("Post not found")


def delete_post(PostID):
    post = session.query(Posts).filter_by(PostID=PostID).first()
    if post:
        session.delete(post)
        session.commit()
        print("Post deleted")
    else:
        print("Post not found")


def is_authorized_to_edit_comment(userID, postID, commentID):
    comment = session.query(Comments).filter_by(PostID=postID, CommentID=commentID).first()
    if comment:
        if comment.UserID == userID:
            return True
    return False


def edit_comment(userID, postID, commentID, new_content):
    comment = session.query(Comments).filter_by(UserID=userID, PostID=postID, CommentID=commentID).first()
    if comment:
        comment.CommentContent = new_content
        session.commit()
        print("Comment updated")
    else:
        print("Comment not found")


def delete_comment(userID, postID, CommentID):
    comment = session.query(Comments).filter_by(UserID=userID, PostID=postID, CommentID=CommentID).first()
    if comment:
        session.delete(comment)
        session.commit()
        print("Comment deleted")
    else:
        print("Comment not found")


def count_likes(PostID):
    likes_count = session.query(Likes).filter_by(PostID=PostID).count()
    return likes_count


def edit_user_name(userID, new_first_name, new_last_name):
    user = session.query(Users).filter_by(userID=userID).first()
    if user:
        user.FirstName = new_first_name
        user.LastName = new_last_name
        session.commit()
        print("User name updated")
    else:
        print("User not found")


def login(email, password):
    user = session.query(Users).filter_by(Email=email).first()
    if user and user.check_password(password):
        print("Login successful")
        return user
    else:
        print("Invalid email or password")
        return None


def count_followers(userID):
    followers_count = session.query(Follows).filter_by(FolloweeID=userID).count()
    return followers_count


def count_follows(userID):
    follows_count = session.query(Follows).filter_by(FollowerID=userID).count()
    return follows_count


db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

# Create the database engine
db = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
engine = create_engine(db)

# Create all tables known to Base
Base.metadata.create_all(engine)

# Create a new session
Session = sessionmaker(bind=engine)
session = Session()
