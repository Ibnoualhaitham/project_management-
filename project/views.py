from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Project, ProjectManager, Task, Comment
from .forms import RegisterForm  # You might need to create forms.py
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
import uuid
from django.http import Http404


# User Authentication
class RegistrationView(CreateView):
    form_class = RegisterForm
    template_name = "register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        messages.success(self.request, "Registration successful!")
        return redirect(self.success_url)


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = "login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("project_list")
    success_message = "Login successful!"


class UserLogoutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy("login")

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, "Logout successful!")
        return response


# Profile page
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "user_profile.html"
    context_object_name = "user"


# Home Views
class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    context_object_name = "project_admin"  # Changed from project_admin to project_list
    template_name = "project_list.html"

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    context_object_name = "project_admin"
    template_name = "project_detail.html"


class ProjectCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Project
    fields = ["title", "description", "comments", "members", "project_admin", "tasks", "priority", "start_date", "end_date", "status","is_completed",
    ]
    template_name = "create_project.html"
    success_url = reverse_lazy("project_list")
    success_message = "Project created successfully"

    def form_valid(self, form):
        form.instance.project_admin = self.request.user
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Project
    fields = ["title", "description", "comments", "members", "project_admin", "tasks","priority", "start_date", "end_date", "status", "is_completed",]
    template_name = "create_project.html"
    success_url = reverse_lazy("project_list")
    success_message = "project updated successfully"

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Project, id=pk)


class ProjectDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Project
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("project_list")
    success_message = "Project deleted successfully"

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Project, id=pk)


# Task Views
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "task_list.html"

    def get_queryset(self):
        """
        Returns the tasks associated with the projects the current user is a member of.
        """
        user = self.request.user
        # Get projects the user is a member of.
        projects = Project.objects.filter(members=user)
        # Get tasks associated with those projects.
        tasks = Task.objects.filter(project__in=projects).order_by(
            "created_at"
        )  # Order by created_at or any other relevant field
        return tasks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #  Get the project admin for each task.  This is complex because of the ManyToManyField.
        #  A Task is in a Project.  A Project has one admin.
        project_admins = {}
        for task in context["tasks"]:
            # Find the projects that include this task.  There could be more than one.
            projects = Project.objects.filter(tasks=task)
            if projects.exists():
                # Get the admin of the first project found.
                project_admins[task.id] = projects.first().project_admin
            else:
                project_admins[task.id] = "No Project"  # Or some other default
        context["project_admins"] = project_admins
        return context


# Task Create View
class TaskCreateView(LoginRequiredMixin, CreateView):

    model = Task
    fields = ["title", "description", "comments", "status", "priority", "assignee"]
    template_name = "create_task.html"
    success_url = reverse_lazy("task_list")

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project_id"] = self.kwargs.get(
            "project_id"
        )  # Pass the project id.
        return context


# Task Update View
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ["title", "description", "comments", "status", "priority", "assignee"]
    template_name = "task_form.html"
    success_url = reverse_lazy("task_list")

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(project__members=user)


# Task Delete View
class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("task_list")

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(project__members=user)