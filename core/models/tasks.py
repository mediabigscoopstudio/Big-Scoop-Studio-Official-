from django.db import models
from core.models.users import User
from core.models.project import Project


class Task(models.Model):

    STATUS_CHOICES = (
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('review', 'Review'),
        ('completed', 'Completed'),
    )

    INTENSITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')

    # Can be assigned to any user
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tasks')

    title = models.CharField(max_length=255)
    description = models.TextField()

    intensity = models.CharField(max_length=20, choices=INTENSITY_CHOICES, default='medium')

    deadline = models.DateTimeField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.project.name}"