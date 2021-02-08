from django.db import models
from src.user.models import User
from src.group.models import Group


class Repository(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    about = models.TextField()
    group_fk = models.ForeignKey(Group, on_delete=models.DO_NOTHING)

    def __int__(self):
        return self.id


class Branch(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    user_fk = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    repository_fk = models.ForeignKey(Repository, on_delete=models.CASCADE)
    is_master = models.BooleanField()

    def __int__(self):
        return self.id


class Commit(models.Model):
    id = models.BigAutoField(primary_key=True)
    changes = models.BigIntegerField()
    branch_fk = models.ForeignKey(Branch, on_delete=models.CASCADE)
    user_fk = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    commit_time = models.BigIntegerField()
    message = models.TextField()

    def __int__(self):
        return self.id


class Column(models.Model):
    id = models.BigAutoField(primary_key=True)
    branch_fk = models.ForeignKey(Branch, on_delete=models.CASCADE)
    name = models.TextField()

    def __int__(self):
        return self.id


class Row(models.Model):
    id = models.BigAutoField(primary_key=True)
    column_fk = models.ForeignKey(Column, on_delete=models.CASCADE)
    content = models.TextField()

    def __int__(self):
        return self.id
