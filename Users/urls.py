from django.urls import include, path
from .views import *
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('',ViewTest)

urlpatterns = [
    path("", include(router.urls)),
]
