from django.urls import path
from .views import WeightListView, WeightDetailView, DailyWeightGainView, AllWeightGainView, GroupDailyGainView,GroupAllWeightGainView

urlpatterns = [
    path('weights/', WeightListView.as_view(), name='weight-list'),
    path('weights/<int:pk>/', WeightDetailView.as_view(), name='weight-detail'),
    path('weights/daily-gain/<int:animal_id>/', DailyWeightGainView.as_view(), name='daily-weight-gain'),
    path('weights/all-gain/<int:animal_id>/', AllWeightGainView.as_view(), name='all-gain'),
    path('weights/group-daily-gain/<int:group_id>/', GroupDailyGainView.as_view(), name='group-daily-gain'),
    path('weights/group-all-gain/<int:group_id>/', GroupAllWeightGainView.as_view(), name='group-all-gain'),
]
