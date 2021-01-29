from sqlalchemy import BigInteger, Text, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class FormFieldContent(Base):
    __tablename__ = "form_field_content"
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    content = Column(Text)
    form_field_fk = Column(BigInteger, ForeignKey="form_field.id")
