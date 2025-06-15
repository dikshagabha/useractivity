import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from activitylog.models import UserActivityLog
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def auth_user(api_client):
    user = User.objects.create_user(username='testuser', password='testpass')
    token = RefreshToken.for_user(user).access_token
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return user

@pytest.mark.django_db
def test_post_create_activity_log(api_client, auth_user):
    response = api_client.post('/api/user-activity/', {
        'action': 'LOGIN',
        'metadata': {'ip': '127.0.0.1'},
        'status': 'PENDING'
    }, format='json')
    assert response.status_code == 201

@pytest.mark.django_db
def test_get_user_activity_logs(api_client, auth_user):
    UserActivityLog.objects.create(user=auth_user, action='LOGIN', status='DONE')
    response = api_client.get(f'/api/user-activity/{auth_user.id}/')
    assert response.status_code == 200
    assert len(response.data) == 1

@pytest.mark.django_db
def test_filter_logs_by_action(api_client, auth_user):
    UserActivityLog.objects.create(user=auth_user, action='LOGIN', status='DONE')
    UserActivityLog.objects.create(user=auth_user, action='LOGOUT', status='DONE')
    response = api_client.get('/api/user-activity/all/?action=LOGIN')
    assert response.status_code == 200
    for log in response.data:
        assert log['action'] == 'LOGIN'

@pytest.mark.django_db
def test_patch_update_status(api_client, auth_user):
    log = UserActivityLog.objects.create(user=auth_user, action='LOGIN', status='PENDING')
    response = api_client.patch(f'/api/user-activity/update/{log.id}/', {
        'status': 'DONE'
    }, format='json')
    assert response.status_code == 200
    assert response.data['status'] == 'DONE'

@pytest.mark.django_db
def test_permissions(api_client):
    user1 = User.objects.create_user(username='user1', password='pass')
    user2 = User.objects.create_user(username='user2', password='pass')
    log = UserActivityLog.objects.create(user=user1, action='LOGIN', status='PENDING')
    token = RefreshToken.for_user(user2).access_token
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    response = api_client.get(f'/api/user-activity/{user1.id}/')
    assert response.status_code in [403, 200] and len(response.data) == 0

