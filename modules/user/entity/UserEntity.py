from sqlalchemy import BigInteger, Text, Column, ForeignKey


class User:
    __tablename__ = "user"
    name = Column(Text)
    email = Column(Text)
    phone = Column(Text)
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    about = Column(Text, nullable=True)
    birth = Column(BigInteger)
    nationality = Column(Text)
    study = Column(Text)
    pic = Column(Text)
