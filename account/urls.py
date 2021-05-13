from django.urls import path, include
from . import views

urlpatterns = [
    path('account/<int:pk>', views.AccountView.as_view(), name='account_profile'),
    path('account/', include('django.contrib.auth.urls')),
    path('account/register', views.RegisterView.as_view(), name='app_register'),
]
