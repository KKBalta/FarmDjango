from django.urls import path
from .views import FarmerListView, FarmerDetailView ,CompanyDetailView,CompanyListView

urlpatterns = [
    path('farmers/', FarmerListView.as_view(), name='farmer-list'),
    path('farmers/<int:pk>/', FarmerDetailView.as_view(), name='farmer-detail'),
    path('company/',CompanyListView.as_view(), name='company-list'),
    path('company/<int:pk>', CompanyDetailView.as_view(),name= 'company-detail')
]
