from django.urls import include, path
from .views import *

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
     path('chart/', chart_data, name='chart_data'),
]