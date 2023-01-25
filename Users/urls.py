from django.urls import include, path
from .views import *
from rest_framework.routers import DefaultRouter,SimpleRouter

routerMain=DefaultRouter()
routerMain.register('main',ViewTest)

routerActlog=DefaultRouter()
routerActlog.register('act',ActivityLogView)



# router.register('norA',norA)
urlpatterns = [
    path("", include(routerMain.urls)),
    path("", include(routerActlog.urls)),
]
