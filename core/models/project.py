from django.db import models
from core.models.users import User
from core.models.accounts import Client


class Project(models.Model):

    STATUS_CHOICES = (
        ('planning', 'Planning'),
        ('active', 'Active'),
        ('on_hold', 'On Hold'),
        ('completed', 'Completed'),
    )

    # ================= BASIC =================

    title = models.CharField(max_length=255)

    slug = models.SlugField(
        unique=True,
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    # ================= CLIENT =================

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='projects'
    )

    # ================= TEAM =================

    managers = models.ManyToManyField(
        User,
        related_name='managed_projects',
        limit_choices_to={'role': 'manager'},
        blank=True
    )

    staff_members = models.ManyToManyField(
        User,
        related_name='staff_projects',
        limit_choices_to={'role': 'staff'},
        blank=True
    )

    # ================= BRANDING =================

    logo = models.ImageField(
        upload_to='project_logos/',
        blank=True,
        null=True
    )

    primary_color = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    secondary_color = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    # ================= FINANCIAL =================

    project_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    gst_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=18
    )

    advance_paid = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    remaining_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    # ================= DATES =================

    start_date = models.DateField()

    deadline = models.DateField()

    # ================= STATUS =================

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='planning'
    )

    # ================= TIMESTAMP =================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.title