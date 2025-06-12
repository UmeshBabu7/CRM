from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from django.contrib.auth.views import (
    LoginView, 
    LogoutView, PasswordResetView, 
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from .views import(
    LandingPageView,LeadListView,LeadDetailView,leadCreateView,LeadUpdateView,LeadDeleteView,SignupView, AssignAgentView,CategoryListView
)

app_name='leads'

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing-page'),
    path('list/', LeadListView.as_view(), name='lead-list'),
    path('<int:pk>/', LeadDetailView.as_view(), name='lead-detail'),
    path('<int:pk>/update/', LeadUpdateView.as_view(), name='lead-update'),
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
    path('create/', leadCreateView.as_view(), name='lead-create'),

    path('<int:pk>/assign-agent/', AssignAgentView.as_view(), name='assign-agent'),

    path('categories/', CategoryListView.as_view(), name='category-list'),

    path('signup/',SignupView.as_view(),name='signup'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),

    path('reset-password/', PasswordResetView.as_view(), name='reset-password'),
    path('password-reset-done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
