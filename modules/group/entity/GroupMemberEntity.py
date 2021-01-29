from sqlalchemy import BigInteger, Text, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class GroupMember(Base):
    __tablename__ = "group_member"

    group_fk = Column(BigInteger, ForeignKey="group.id")
    user_fk = Column(BigInteger, ForeignKey="user.id")

    role = Column(Text)
