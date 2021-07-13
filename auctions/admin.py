from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Bid, Comment, ActiveListing, User
# Register your models here.
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(ActiveListing)
admin.site.register(User)

