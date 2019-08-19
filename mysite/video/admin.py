from django.contrib import admin
from .models import Film,user_filmlist,Comment
# Register your models here.
admin.site.register(Film)
admin.site.register(user_filmlist)
admin.site.register(Comment)