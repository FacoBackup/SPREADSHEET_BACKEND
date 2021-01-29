from sqlalchemy import BigInteger, Text, Column, ForeignKey


class Group:
    __tablename__ = "group"
    name = Column(Text)
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    about = Column(Text)
