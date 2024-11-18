# animal/urls.py
from django.urls import path
from .views import AnimalListView, AnimalDetailView

urlpatterns = [
    path('animals/', AnimalListView.as_view(), name='animal-list'),
    path('animals/<int:pk>/', AnimalDetailView.as_view(), name='animal-detail'),
]
