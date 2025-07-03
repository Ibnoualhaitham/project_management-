from django.contrib import admin

# Register your models here.

from project.models import Project, Task, Comment

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Comment)