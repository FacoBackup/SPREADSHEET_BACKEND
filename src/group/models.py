from django.db import models


class Group(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    pic = models.TextField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)

    def __int__(self):
        return self.id
