from django.contrib import admin
from users.models import SchoolUser


@admin.register(SchoolUser)
class AdminSchoolUser(admin.ModelAdmin):
    list_filter = ('id', 'email')
