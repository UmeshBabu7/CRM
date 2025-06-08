from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import (
    LandingPageView,
    LeadListView, LeadDetailView,leadCreateView, LeadUpdateView, LeadDeleteView,SignupView
)

app_name='leads'

urlpatterns = [
      path('', LandingPageView.as_view(), name='landing-page'),
    path('list/', LeadListView.as_view(), name='lead-list'),
    path('<int:pk>/', LeadDetailView.as_view(), name='lead-detail'),
    path('<int:pk>/update/', LeadUpdateView.as_view(), name='lead-update'),
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
    path('create/', leadCreateView.as_view(), name='lead-create'),

    path('signup/',SignupView.as_view(),name='signup'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout')
]
