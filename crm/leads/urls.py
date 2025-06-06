from django.urls import path
from .views import *

app_name='leads'

urlpatterns = [
    path('list/',lead_list,name='lead-list'),
    path('detail/<int:id>/',lead_detail,name='lead-detail'),
    path('create/',lead_create,name='lead-create'),
    path('update/<int:id>/',lead_update,name='lead-update'),
    path('delete/<int:id>/',lead_delete,name='lead-delete'),
    path('',landing_page,name='landing-page')
]
