from django.db import models


class User(models.Model):
    db_table = '"user"'
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    email = models.CharField(max_length=320, unique=True)
    phone = models.CharField(max_length=120, unique=True)
    pic = models.TextField(null=True, blank=True)
    birth = models.PositiveBigIntegerField()
    nationality = models.TextField()
    study = models.CharField(max_length=512)
    about = models.TextField(null=True, blank=True)

    def __int__(self):
        return self.id
