
from django.urls import path
from .views import login_view, logout_view , search_view,test_view, api_login_view, signup_view, add_spam_view, view_spammers_view
from rest_framework_simplejwt import views as jwt_views
# Path defined for the API views
urlpatterns = [
    path('api/test/', test_view, name='test_view'),

    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', login_view, name='login'),  
    path('api/login/', api_login_view, name='api_login'),
    path('signup/', signup_view, name='signup'),  
    path('api/add-spam/', add_spam_view, name='add_spam'),
    path('api/view-spammers/', view_spammers_view, name='view_spammers'),
    path('logout/', logout_view, name='logout'), 
    path('search/', search_view, name='search'),

    
]



