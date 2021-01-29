from sqlalchemy import BigInteger, Text, Column


class Form:
    __tablename__ = "form"
    name = Column(Text)
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    creation_date = Column(BigInteger)
    group_fk = Column(BigInteger, ForeignKey="group.id")
