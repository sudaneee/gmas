from django.urls import path
from . import views


urlpatterns = [
    path('', views.fees_index, name='fees_index'),
    path('fees_activation', views.fees_activation, name='fees_activation'),
    path('fees_record', views.fees_record, name='fees_record'),
]