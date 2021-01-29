from sqlalchemy import BigInteger, Text, Column, ForeignKey


class FormFieldContent:
    __tablename__ = "form_field_content"
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    content = Column(Text)
    form_field_fk = Column(BigInteger, ForeignKey="form_field.id")
