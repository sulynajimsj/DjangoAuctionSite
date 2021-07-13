from typing import Callable
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.fields import BooleanField, CharField, DateField, DateTimeField, IntegerField, TextField, URLField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.forms.widgets import Textarea

class User(AbstractUser):
    watchlist = ManyToManyField("ActiveListing", blank=True, related_name="theuser")

class Bid(models.Model):
    amount = IntegerField()
    user = ForeignKey(User, blank=False, on_delete=CASCADE, related_name="thebid")

class Comment(models.Model):
    thecomment = TextField()
    date = DateTimeField()
    user = ForeignKey(User, related_name="uuser", blank=False, on_delete=CASCADE)

class ActiveListing(models.Model):
    title = CharField(max_length=65)
    des = TextField(default="No description")
    date = DateTimeField()
    bid = ForeignKey(Bid, on_delete = PROTECT, related_name="thelisting")
    image = URLField(blank=True)
    category = CharField(max_length=40, blank=True)
    user = ForeignKey(User, related_name="user", blank=False, on_delete=CASCADE)
    status = BooleanField(default=True)
    comments = ManyToManyField(Comment, blank=True, related_name="listing")

    


