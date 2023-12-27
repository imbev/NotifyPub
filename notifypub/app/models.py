from django.db import models


# Create your models here.

class Message(models.Model):
    title = models.CharField()
    summary = models.CharField()
    content = models.CharField()
    create_date = models.DateTimeField("date created")

    def __str__(self):
        return f"{self.title} ({self.create_date})"


class Token(models.Model):
    description = models.CharField()
    token = models.CharField()
    create_date = models.DateTimeField("date created")

    def __str__(self):
        return f"{self.description} ({self.create_date})"