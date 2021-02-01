from django.db import models


class Form(models.Model):
    db_table = '"form"'
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    about = models.TextField(null=True, blank=True)

    def __int__(self):
        return self.id
