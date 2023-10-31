from django.contrib import admin
from .models import Category, RequestCategory, Users, SellRequest

admin.site.register(Category)
admin.site.register(RequestCategory)
admin.site.register(Users)
admin.site.register(SellRequest)
