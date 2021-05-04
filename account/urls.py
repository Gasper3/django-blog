from django.urls import path, include
from .views import RegisterView

urlpatterns = [
    path('account/<str:username>', RegisterView.as_view(), name='account_profile'),
    path('account/', include('django.contrib.auth.urls')),
    path('account/register', RegisterView.as_view(), name='app_register'),
]
