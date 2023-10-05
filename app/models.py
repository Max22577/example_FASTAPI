from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship
from .database import Base



class Post(Base):
    __tablename__ = "Post"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone = True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("User.id", ondelete="CASCADE"),nullable=False)
    phone_number = Column(Integer, nullable=False)
    
    owner = relationship("User")
    
class User(Base):
    __tablename__ = "User"
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable= False)
    created_at = Column(TIMESTAMP(timezone = True), nullable=False, server_default=text('now()'))
    
class Vote(Base):
    __tablename__  = "Votes"
    
    user_id = Column(Integer, ForeignKey("User.id", ondelete="CASCADE"), primary_key=True)
    posts_id = Column(Integer, ForeignKey("Post.id", ondelete="CASCADE"), primary_key=True)