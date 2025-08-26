from django.urls import path
from .views import HomeView, FlightCreateView, FlightListView, FlightStatsView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path('flights/create/', FlightCreateView.as_view(), name='flight-create'),
    path('flights/', FlightListView.as_view(), name='flight-list'),
    path('flights/stats/', FlightStatsView.as_view(), name='flight-stats'),
]