# Slaughter/urls.py
from django.urls import path
from .views import SlaughterListView, SlaughterDetailView

urlpatterns = [
    path('slaughters/', SlaughterListView.as_view(), name='slaughter-list'),
    path('slaughters/<int:pk>/', SlaughterDetailView.as_view(), name='slaughter-detail'),
]
