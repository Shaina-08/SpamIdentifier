from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .forms import SignupForm, LoginForm
from django.db.models import Case, When, Value, IntegerField, F
from .utils import get_number_info 
from rest_framework_simplejwt.tokens import RefreshToken
import json
from django.db.models.functions import Lower
from django.middleware.csrf import get_token
from .models import Spam, Contact
from django.db.models import Q
# Signup View
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Signup successful. You are now logged in.')
            return redirect('add_spam')
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'signup.html', {'form': form}, status=400)
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            password = form.cleaned_data.get('password')
            user = authenticate(request, phone_number=phone_number, password=password)
            if user is not None:
                auth_login(request, user)
                refresh = RefreshToken.for_user(user)
                response = JsonResponse({
                    'status': 'success',
                    'message': 'Login successful',
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                })
                return redirect('add_spam')
            else:
                messages.error(request, 'Invalid phone number or password.')
                return render(request, 'login.html', {'form': form}, status=400)
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'login.html', {'form': form}, status=400)
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@csrf_exempt 
@login_required
def add_spam_view(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User not authenticated'}, status=401)

        phone_number = request.POST.get('phone_number')
        
        if not phone_number:
            return JsonResponse({'error': 'Please provide a phone number.'}, status=400)

        number_info = get_number_info(phone_number)
        
        if not number_info:
            return JsonResponse({'error': 'Number information could not be retrieved.'}, status=404)

        spam, created = Spam.objects.get_or_create(phone_number=phone_number, reported_by=request.user)
        
        if created:
            return JsonResponse({'message': 'Number added to spam list successfully.'}, status=201)
        else:
            return JsonResponse({'message': 'Number is already in the spam list.'}, status=200)

    csrf_token = get_token(request)
    return render(request, 'add_spam.html', {'csrf_token': csrf_token})

@csrf_exempt
@login_required
def view_spammers_view(request):
    spammers = Spam.objects.all()
    spammers_list = []

    for spam in spammers:
        contact = Contact.objects.filter(phone_number=spam.phone_number).first()
        email = contact.user.email if contact else None

        spam_data = {
            'phone_number': spam.phone_number,
            'reported_by': spam.reported_by.name,
            'email': email,
        }

        spammers_list.append(spam_data)

    return JsonResponse({'spammers': spammers_list}, status=200)

@csrf_exempt
@require_POST
def api_login_view(request):
    try:
        data = json.loads(request.body)
        phone_number = data.get('phone_number')
        password = data.get('password')
        user = authenticate(request, phone_number=phone_number, password=password)
        if user is not None:
            auth_login(request, user)
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'status': 'success',
                'message': 'Login successful',
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            })
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid phone number or password'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

@csrf_exempt
@require_POST
def test_view(request):
    return JsonResponse({'message': 'Test successful'}, status=200)

def logout_view(request):
    auth_logout(request)
    return redirect('login')

@csrf_exempt



def search_view(request):
    query = request.GET.get('query', '').strip()
    search_type = request.GET.get('type', '').strip()

    # Validate `query` parameter
    if not query:
        return JsonResponse({'error': 'Query parameter is required and cannot be empty'}, status=400)

    # Validate `search_type` parameter
    valid_search_types = ['phone', 'name']
    if search_type not in valid_search_types:
        return JsonResponse({'error': 'Invalid search type. Allowed values are: phone, name'}, status=400)

    # Perform search based on type
    if search_type == 'phone':
        spam_queryset = Spam.objects.annotate(
            relevance=Case(
                When(phone_number=query, then=Value(2)),
                When(phone_number__icontains=query, then=Value(1)),
                default=Value(0),
                output_field=IntegerField()
            )
        ).order_by('-relevance', 'phone_number')

    elif search_type == 'name':
        spam_queryset = Spam.objects.annotate(
            relevance=Case(
                When(reported_by__name__iexact=query, then=Value(2)),
                When(reported_by__name__icontains=query, then=Value(1)),
                default=Value(0),
                output_field=IntegerField()
            )
        ).order_by('-relevance', Lower('reported_by__name'))

    # Prepare results
    results = [
        {
            'phone_number': spam.phone_number,
            'reported_by': spam.reported_by.name if spam.reported_by else None,
            'is_spam': spam.is_spam, 
            'relevance': spam.relevance
        }
        for spam in spam_queryset
    ]

    return JsonResponse({'results': results}, status=200)