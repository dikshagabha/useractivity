from django.db import models
from django.contrib.auth.models import User
# Custom QuerySet to allow filtering by action and date range
class UserActivityLogQuerySet(models.QuerySet):
	 # Filter logs by activity type (e.g., LOGIN, LOGOUT)
    def by_action(self, action_type):
        return self.filter(action=action_type)

    # Filter logs within a datetime range
    def in_date_range(self, start_date, end_date):
        return self.filter(timestamp__range=(start_date, end_date))

# Custom Manager to expose our custom query methods on the model
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
  
    # Primary key (auto-incremented)
    id = models.AutoField(primary_key=True)

    # ForeignKey to Django’s built-in User model
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')

    # Type of activity (e.g., LOGIN, LOGOUT)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)

    # Time of the activity (indexed for performance)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    # Optional metadata stored in JSON format (e.g., IP, device)
    metadata = models.JSONField(blank=True, null=True)

    # Status of the activity
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    # Attach our custom manager
    objects = UserActivityLogManager()


    def __str__(self):
        return f"{self.user.username} - {self.action} at {self.timestamp}"
