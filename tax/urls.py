
from django.urls import path
from . import views

urlpatterns = [

    # CRUD Operation
    path('create-tax/', views.create_tax, name='create-tax'),
    path('list-tax/', views.list_tax, name='list-tax'),
    path('fetch-tax/<int:id>/', views.view_tax, name='fetch-tax'),
    path('update-tax/<int:id>/', views.update_tax, name='update-tax'),

    # make payment
    path('tax-payment/<int:id>/', views.tax_payment, name='tax-payment'),

    # History
    path('list-tax-history/<int:id>/', views.tax_history, name='tax-history'),
]