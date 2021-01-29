from sqlalchemy import BigInteger, Text, Column, ForeignKey


class FormField:
    __tablename__ = "form_field"
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    name = Column(Text)
    form_fk = Column(BigInteger, ForeignKey="form.id")
