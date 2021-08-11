from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datereceived = models.DateTimeField(null=True, blank=True)
    qty = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Item(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='website/images/')
    url = models.URLField(blank=True)

    def __str__(self):
        return self.title
