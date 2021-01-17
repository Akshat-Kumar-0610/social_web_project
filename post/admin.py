from django.contrib import admin
from .models import post,Comment
from django.contrib.auth import get_user_model
from users.models import Profile
from django.http import HttpResponse
import csv, datetime, xlsxwriter
from import_export.admin import ImportExportModelAdmin
from users.actions import export_as_xls


User = get_user_model()
admin.site.unregister(User)
User = get_user_model()
@admin.register(User)
class Admin(admin.ModelAdmin):
    actions = [export_as_xls]


@admin.register(Comment)
class Comment(admin.ModelAdmin):
    actions = [export_as_xls]  #register the action in your model admin




@admin.register(post)
class post(admin.ModelAdmin):
    actions = [export_as_xls]  #register the action in your model admin


@admin.register(Profile)
class Profile(admin.ModelAdmin):
    actions = [export_as_xls]  #register the action in your model admin



