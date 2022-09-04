from django.db import models

class comment(models.Model):
    post_id = models.IntegerField()
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    telephone = models.CharField(max_length=10)
    localisation = models.CharField(max_length=500)
