from django.db import models
from src.group.models import Group
from src.user.models import User


class GroupMembership(models.Model):
    db_table = '"group_membership"'
    group_fk = models.ForeignKey(Group, on_delete=models.CASCADE)
    user_fk = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.TextField()
