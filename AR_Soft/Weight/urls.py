from django.urls import path
from .views import WeightListView, WeightDetailView, DailyWeightGainView

urlpatterns = [
    path('weights/', WeightListView.as_view(), name='weight-list'),
    path('weights/<int:pk>/', WeightDetailView.as_view(), name='weight-detail'),
    path('weights/daily-gain/<int:animal_id>/', DailyWeightGainView.as_view(), name='daily-weight-gain'),
]
