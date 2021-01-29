from sqlalchemy import BigInteger, Text, Column, ForeignKey


class GroupMember:
    __tablename__ = "group_member"

    group_fk = Column(BigInteger, ForeignKey="group.id")
    user_fk = Column(BigInteger, ForeignKey="user.id")

    role = Column(Text)
