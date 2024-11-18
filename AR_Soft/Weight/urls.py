# weight/urls.py
from django.urls import path
from .views import WeightListView, WeightDetailView

urlpatterns = [
    path('weights/', WeightListView.as_view(), name='weight-list'),
    path('weights/<int:pk>/', WeightDetailView.as_view(), name='weight-detail'),
]
