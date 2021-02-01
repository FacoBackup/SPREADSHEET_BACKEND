from django.db import models
from src.user.models import User


class Form(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    about = models.TextField(null=True, blank=True)

    def __int__(self):
        return self.id


class FormAccess(models.Model):
    user_fk = models.ForeignKey(User, on_delete=models.CASCADE)
    form_fk = models.ForeignKey(Form, on_delete=models.CASCADE)


class FormField(models.Model):
    db_table = '"form_field"'
    id = models.BigAutoField(primary_key=True)
    form_fk = models.ForeignKey(Form, on_delete=models.CASCADE)
    name = models.TextField()

    def __int__(self):
        return self.id


class FormContent(models.Model):
    db_table = '"form_content"'
    field_fk = models.ForeignKey(FormField, on_delete=models.CASCADE)
    content = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __int__(self):
        return self.field_fk
