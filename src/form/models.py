from django.db import models
from src.user.models import User
from src.group.models import Group


class Form(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField(unique=True)
    about = models.TextField(null=True, blank=True)
    group_fk = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    creator_fk = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __int__(self):
        return self.id


class FormAccess(models.Model):
    user_fk = models.ForeignKey(User, on_delete=models.CASCADE)
    form_fk = models.ForeignKey(Form, on_delete=models.CASCADE)


class FormField(models.Model):
    id = models.BigAutoField(primary_key=True)
    form_fk = models.ForeignKey(Form, on_delete=models.CASCADE)
    name = models.TextField()

    def __int__(self):
        return self.id


class FormContent(models.Model):
    id = models.BigAutoField(primary_key=True)
    field_fk = models.ForeignKey(FormField, on_delete=models.CASCADE)
    content = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __int__(self):
        return self.id
