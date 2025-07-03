from django.urls import path
from .views import (
   ProjectListCreate,
   ProjectRetrieveUpdateDestroy,
   TaskListCreate,
   TaskRetrieveUpdateDestroy,
   CommentListCreate,
   CommentRetrieveUpdateDestroy,
   ProjectViewSet,
   TaskViewSet,
   CommentViewSet,
)

urlpatterns = [
   
    path('v2/projects/', ProjectListCreate.as_view(), name='project-list'),
    path('v2/projects/<int:pk>/', ProjectRetrieveUpdateDestroy.as_view(), name='project-detail'),

   
    path('v2/tasks/', TaskListCreate.as_view(), name='task-list'),
    path('v2/tasks/<int:pk>/', TaskRetrieveUpdateDestroy.as_view(), name='task-detail'),

    path('v2/comments/', CommentListCreate.as_view(), name='comment-list'),
    path('v2/comments/<int:pk>/', CommentRetrieveUpdateDestroy.as_view(), name='comment-detail'),
]