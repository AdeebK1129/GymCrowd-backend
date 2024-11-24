from django.urls import path
from apps.gyms.views import GymListView, GymDetailView, CrowdDataListView, CrowdDataDetailView

urlpatterns = [
    path("", GymListView.as_view(), name="gym-list"),
    path("<int:id>/", GymDetailView.as_view(), name="gym-detail"),
    path('crowddata/', CrowdDataListView.as_view(), name='crowddata-list'),
    path('crowddata/<int:pk>/', CrowdDataDetailView.as_view(), name='crowddata-detail'),
]
