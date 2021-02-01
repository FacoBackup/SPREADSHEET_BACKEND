from django.db import models
from src.user.models import User


class Group(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField(unique=True)
    pic = models.TextField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)

    def __int__(self):
        return self.id


class GroupMembership(models.Model):
    group_fk = models.ForeignKey(Group, on_delete=models.CASCADE)
    user_fk = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.TextField()

    def __int__(self):
        return self.user_fk
