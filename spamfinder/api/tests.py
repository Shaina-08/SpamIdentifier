import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth import get_user_model
from .models import Spam
import json

User = get_user_model()

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def user():
    return User.objects.create_user(
        phone_number='1234567890',
        password='password123',
        email='test@example.com',
        name='Test User'
    )


@pytest.mark.django_db
def test_login_view_success(client, user):
    url = reverse('login')
    response = client.post(url, {
        'phone_number': user.phone_number,
        'password': 'password123'
    })
    assert response.status_code == 302  
    assert 'sessionid' in client.cookies 

@pytest.mark.django_db
def test_login_view_failure(client):
    url = reverse('login')
    response = client.post(url, {
        'phone_number': 'nonexistent',
        'password': 'wrongpassword'
    })
    assert response.status_code == 400  

@pytest.mark.django_db
def test_view_spammers_view(client, user):
    client.login(phone_number=user.phone_number, password='password123')
    Spam.objects.create(phone_number='5555555555', reported_by=user)
    url = reverse('view_spammers')
    response = client.get(url)
    assert response.status_code == 200  # OK
    assert b'5555555555' in response.content  


@pytest.mark.django_db
def test_api_login_view_failure(client):
    url = reverse('api_login')
    response = client.post(url, json.dumps({
        'phone_number': '1234567890',
        'password': 'wrongpassword'
    }), content_type='application/json')
    assert response.status_code == 400  

@pytest.mark.django_db
def test_search_view(client, user):
    Spam.objects.create(phone_number='5555555555', reported_by=user)
    url = reverse('search')
    response = client.get(url, {'query': '5555555555', 'type': 'phone'})
    assert response.status_code == 200  
    response_data = json.loads(response.content)
    assert len(response_data['results']) > 0 

@pytest.mark.django_db
def test_search_view_invalid_type(client):
    url = reverse('search')
    response = client.get(url, {'query': '5555555555', 'type': 'invalid'})
    assert response.status_code == 400 

