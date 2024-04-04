from django.db import models

class Note(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    session = models.CharField(max_length=100, default='default_session')

    def __str__(self):
        return self.title


