from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('createresult', views.resultcreate, name='resultcreate'),
    path('updateresult', views.updateresult, name='updateresult'),
    path('single_result_update', views.single_result_update, name='single_result_update'),
    path('result_view', views.result_view, name='result_view'),
    path('settings', views.settings, name='settings'),
    path('single_result_view', views.single_result_view, name='single_result_view'),
]

