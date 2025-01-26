from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('<user>/', views.DashboardView.as_view(), name='dashboard'),
    path('bilgilerim/<pk>/<user>/', views.MyInformationDashBoardView, name='my_information'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('kayıt-ol', views.RegisterView.as_view(), name='register'),
    path('accounts/password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('dashboard/kayıtlar/', views.LogEntryListView.as_view(), name='logentry_list'),
]
