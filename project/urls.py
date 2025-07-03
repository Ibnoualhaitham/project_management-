from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("project/", views.ProjectListView.as_view(), name="project_list"),
    path("project_detail/<uuid:pk>/", views.ProjectDetailView.as_view(), name='project_detail'),

    # Authentication
    path("", views.UserLoginView.as_view(), name="login"),
    path("register/", views.RegistrationView.as_view(), name="register"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("profile/", views.ProfileView.as_view(), name="user_profile"),

    # Project URLs
    path("project/create/", views.ProjectCreateView.as_view(), name="create_project"),
    path( "project/<uuid:pk>/edit/", views.ProjectUpdateView.as_view(), name="project_edit",),
    path( "project/<uuid:pk>/delete/", views.ProjectDeleteView.as_view(), name="confirm_delete",),

    # Task URLs
    path("tasks/", views.TaskListView.as_view(), name="task_list"),
    path("tasks/create/", views.TaskCreateView.as_view(), name="create_task"),
    path("task/<uuid:pk>/edit/", views.TaskUpdateView.as_view(), name="task_edit"),
    path("tasks/<uuid:pk>/delete/", views.TaskDeleteView.as_view(), name="task_delete",),


]