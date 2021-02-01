from django.db import models
from src.user.models import User
from src.form.models import Form


class FormRole(models.Model):
    db_table = '"form_membership"'
    user_fk = models.ForeignKey(User, on_delete=models.CASCADE)
    form_fk = models.ForeignKey(Form, on_delete=models.CASCADE)
    role = models.TextField()


