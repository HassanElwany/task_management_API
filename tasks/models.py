from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        Group,
        related_name="custom_users",  # Avoid conflicts
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_users",  # Avoid conflicts
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Pending',
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    def mark_complete(self):
        """Mark the task as completed and set the completed_at timestamp."""
        if self.status != 'Completed':
            self.status = 'Completed'
            self.completed_at = now()
            self.save()

    def mark_incomplete(self):
        """Revert the task to pending and clear the completed_at timestamp."""
        if self.status != 'Pending':
            self.status = 'Pending'
            self.completed_at = None
            self.save()

    def clean(self):
        """Validate that the due_date is in the future."""
        if self.due_date and self.due_date < now():
            raise ValidationError("The due date must be in the future.")

    class Meta:
        ordering = ['due_date', 'priority']
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
