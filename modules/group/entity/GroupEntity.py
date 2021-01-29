from sqlalchemy import BigInteger, Text, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Group(Base):
    __tablename__ = "group"
    name = Column(Text)
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    about = Column(Text)
