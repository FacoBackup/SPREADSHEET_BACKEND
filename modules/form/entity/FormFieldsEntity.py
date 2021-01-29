from sqlalchemy import BigInteger, Text, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class FormField(Base):
    __tablename__ = "form_field"
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    name = Column(Text)
    form_fk = Column(BigInteger, ForeignKey="form.id")
