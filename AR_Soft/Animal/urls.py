# animal/urls.py
from django.urls import path
from .views import AnimalListView, AnimalDetailView
from .views import GroupListView, GroupDetailView, AnimalGroupListView, AnimalGroupDetailView


urlpatterns = [
    path('animals/', AnimalListView.as_view(), name='animal-list'),
    path('animals/<int:pk>/', AnimalDetailView.as_view(), name='animal-detail'),
    path('groups/', GroupListView.as_view(), name='group-list'),
    path('groups/<int:pk>/', GroupDetailView.as_view(), name='group-detail'),
    path('animal_groups/', AnimalGroupListView.as_view(), name='animal-group-list'),
    path('animal_groups/<int:pk>/', AnimalGroupDetailView.as_view(), name='animal-group-detail'),

]
