from django.urls import path, include
from .views import RegisterView, AccountView

urlpatterns = [
    path('account/<int:pk>', AccountView.as_view(), name='account_profile'),
    path('account/', include('django.contrib.auth.urls')),
    path('account/register', RegisterView.as_view(), name='app_register'),
]
