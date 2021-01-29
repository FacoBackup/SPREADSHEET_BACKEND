from sqlalchemy import BigInteger, Text, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    name = Column(Text)
    email = Column(Text, unique=True)
    phone = Column(Text, unique=True)
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    about = Column(Text, nullable=True)
    birth = Column(BigInteger)
    nationality = Column(Text)
    study = Column(Text)
    pic = Column(Text, nullable=True)
