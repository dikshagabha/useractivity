# tests/test_models.py
import pytest
from django.contrib.auth.models import User
from activitylog.models import UserActivityLog
from django.core.exceptions import ValidationError
import json

@pytest.mark.django_db
def test_create_user_activity_log():
    user = User.objects.create_user(username='testuser', password='pass')
    log = UserActivityLog.objects.create(
        user=user,
        action='LOGIN',
        metadata={'ip': '127.0.0.1', 'device': 'Mac'},
        status='PENDING'
    )
    assert log.pk is not None
    assert log.status == 'PENDING'

@pytest.mark.django_db
def test_metadata_json_field():
    user = User.objects.create_user(username='testuser', password='pass')
    metadata = {'ip': '127.0.0.1', 'browser': 'Firefox'}
    log = UserActivityLog.objects.create(user=user, action='LOGIN', metadata=metadata)
    assert isinstance(log.metadata, dict)
    assert log.metadata['ip'] == '127.0.0.1'

@pytest.mark.django_db
def test_invalid_status_value():
    user = User.objects.create_user(username='testuser', password='pass')
    with pytest.raises(ValidationError):
        log = UserActivityLog(
            user=user, action='LOGIN', metadata={}, status='INVALID_STATUS'
        )
        log.full_clean()  # Triggers validation
