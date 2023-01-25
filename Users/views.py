# Create your views here.
from rest_framework.viewsets import ModelViewSet
from .permissions import *
from .models import *
from rest_framework import serializers
from rest_framework import permissions
from django_filters import rest_framework as filters



class MainSerializer(serializers.ModelSerializer):
    class Meta: 
        model=TestDisasterModel
        fields="__all__"      
         
class ViewTest(ModelViewSet):
      permission_classes=[CustomObjectLevel]
      queryset= TestDisasterModel.objects.all()   
      
      serializer_class=MainSerializer    
      filter_backends=[filters.DjangoFilterBackend]
      filterset_fields = ['municipality__name','ward__name']

#         filterset_fields = ['municipality__palika']

# class DisasterMunicipalityWise(generics.ListAPIView):
#         queryset=Disaster.objects.all()
#         serializer_class=DisasterSerializer
        
#         # filter_backends=[filters.DjangoFilterBackend,]
#         # filterset_fields = ['municipality__municipality','palika']
#         # search_fields = ['name','municipality__local']
#         # ordering_fields=['name','municipality__local']
        
#         filter_backends=[filters.DjangoFilterBackend,rest_filters.SearchFilter,rest_filters.OrderingFilter]
#         filterset_fields = ['municipality__palika']
#         search_fields = ['name','municipality__local']
#         ordering_fields=['name','municipality__local']