from django.contrib import admin
from django.urls import path
from . import views
from .views import MyTokenObtainPairView


from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [

    # for login
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    # for registration 
    path('tax-payer/', views.create_tax_payer, name='create-tax-payer'),
    path('tax-accountant/', views.create_tax_accountant, name='create-tax-accountant'),


    # for other logic
    path('list-tax-payers/', views.list_tax_payers, name='list-tax-payers'),
]