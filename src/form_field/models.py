from django.db import models
from src.form.models import Form


class FormField(models.Model):
    db_table = '"form_field"'
    id = models.BigAutoField(primary_key=True)
    form_fk = models.ForeignKey(Form, on_delete=models.CASCADE)
    name = models.TextField()
