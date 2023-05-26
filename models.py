from database import Base
from sqlalchemy import String,Boolean,Integer,Column, Text, Date, ForeignKey
from sqlalchemy.orm import relationship


class Restaurant(Base):
    __tablename__ = 'restaurant'
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String(255), nullable=False,unique=True)
    place = Column(Text)


class Menus(Base):
    __tablename__ = 'menus'
    id = Column(Integer,primary_key=True, index=True)
    menu_item = Column(Text)
    price = Column(Integer)
    date = Column(Date)
    resto_id = Column(Integer, ForeignKey("restaurant.id", ondelete="CASCADE"))

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String(255), nullable=False,unique=True)
    email = Column(String)
    password = Column(String)
    position = Column(String)

    
class Voting(Base):
    __tablename__ = 'vote'
    id = Column(Integer,primary_key=True, index=True)
    vote= Column(Boolean)
    date = Column(Date)
    menu_id = Column(Integer, ForeignKey("menus.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    
class VotingNew(Base):
    __tablename__ = 'voting'
    id = Column(Integer,primary_key=True, index=True)
    vote= Column(Integer)
    date = Column(Date)
    menu_id = Column(Integer, ForeignKey("menus.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))