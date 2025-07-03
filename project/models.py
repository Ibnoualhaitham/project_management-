
import uuid
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

TASK_STATUS_CHOICES = [
    ('todo', 'To Do'),
    ('progress', ' In Progress'),
    ('review', 'In Review'),
    ('done', 'Done')
]
PRIORITY_CHOICES = [
    ('med', 'Medium'),
    ('low', 'Low'),
    ('high', "High")
]
PROJECT_STATUS_CHOICES = [
    ('todo', 'To do'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
    ('on_hold', 'On Hold')
]


class BaseMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False, null=True, blank=True)
    
    class Meta:
        abstract = True


class Comment(BaseMixin):
    title = models.CharField(max_length=250)
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    
    
class Task(BaseMixin):
    title = models.CharField(max_length=250)
    description = models.TextField()    
    comments = models.ManyToManyField(Comment, blank=True)
    status = models.CharField( max_length=50, choices=TASK_STATUS_CHOICES, default='todo')
    priority = models.CharField( max_length=50, choices=PRIORITY_CHOICES, default='med')   
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.title
    

class ProjectManager(models.Manager):
   def for_user(self, user):
     return self.filter(Q(project_admin=user) | Q(members__id__in=[user.id])).distinct()
   
    
class Project(BaseMixin):
    title = models.CharField(max_length=200)
    description = models.TextField()   
    comments = models.ManyToManyField(Comment, blank=True)
    members = models.ManyToManyField(User, related_name="projects")
    project_admin  = models.ForeignKey(User, on_delete=models.CASCADE)
    tasks = models.ManyToManyField(Task, blank=True)
    priority = models.CharField( max_length=50, choices=PRIORITY_CHOICES, default='med')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=PROJECT_STATUS_CHOICES, default='todo')
    is_completed = models.BooleanField(default=False)
    
    objects = ProjectManager()

    def __str__(self):
        return self.title