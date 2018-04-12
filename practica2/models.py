from django.db import models

# Create your models here.

class Pages(models.Model):
    name = models.CharField(max_length=64)
    page = models.TextField()

    def __str__(self):
        return str(self.id) + ". " + self.name
