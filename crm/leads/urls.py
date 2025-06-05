from django.urls import path
from .views import *

app_name='leads'

urlpatterns = [
    path('list/',lead_list,name='lead_list'),
    path('detail/<int:id>/',lead_detail,name='lead_detail'),
    path('create/',lead_create,name='lead_create'),
    path('update/<int:id>/',lead_update,name='lead_update')
]
