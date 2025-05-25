from django.urls import path
from .import views

app_name="leads"

urlpatterns = [
    path('leads/',views.lead_list,name='list'),
    path('detail/<int:id>/',views.lead_detail,name='detail')
]
