from django.db import models
from src.user.models import User
from src.form_field.models import FormField


class FormContent(models.Model):
    db_table = '"form_content"'
    field_fk = models.ForeignKey(FormField, on_delete=models.CASCADE)
    content = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
