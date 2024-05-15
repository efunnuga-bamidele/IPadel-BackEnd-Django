
from django.urls import path, include
from rest_framework.authtoken import views
from .views import home


urlpatterns = [
    path('', home, name='api.home'),
    path('court/', include('api.court.urls')),
    path('match/', include('api.match.urls')),
    path('user/', include('api.user.urls')),
    path('email/', include('api.email.urls')),
    path('password/', include('api.password.urls')),
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
]
