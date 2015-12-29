from django.contrib import admin

from . import models


class AuthorAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Lecturer, AuthorAdmin)
admin.site.register(models.Group)
admin.site.register(models.Student)
admin.site.register(models.Test)
admin.site.register(models.Question)
admin.site.register(models.Answer)

