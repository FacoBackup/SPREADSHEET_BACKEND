from sqlalchemy import BigInteger, Text, Column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Form(Base):
    __tablename__ = "form"
    name = Column(Text)
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    creation_date = Column(BigInteger)
    group_fk = Column(BigInteger, ForeignKey="group.id")
