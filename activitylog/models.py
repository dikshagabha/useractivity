from django.db import models
from django.contrib.auth.models import User

class UserActivityLogQuerySet(models.QuerySet):
    def by_action(self, action_type):
        return self.filter(action=action_type)

    def in_date_range(self, start_date, end_date):
        return self.filter(timestamp__range=(start_date, end_date))


class UserActivityLogManager(models.Manager):
    def get_queryset(self):
        return UserActivityLogQuerySet(self.model, using=self._db)

    def by_action(self, action_type):
        return self.get_queryset().by_action(action_type)

    def in_date_range(self, start_date, end_date):
        return self.get_queryset().in_date_range(start_date, end_date)


class UserActivityLog(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Done'),
    ]

    ACTION_CHOICES = [
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('UPLOAD_FILE', 'Upload File'),
        ('PASSWORD_RESET', 'Password Reset'),
        # Add more as needed
    ]
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"{self.user.username} - {self.action} at {self.timestamp}"
