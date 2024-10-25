
from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('me/', views.UsersMe.as_view(), name='users-me'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password/change/', views.ChangePasswordView.as_view(), name='change-password'),
    path('password/forgot/', views.ForgotPasswordView.as_view(), name='forgot-password'),
    path('password/forgot/verify/<str:otp_secret>/', views.ForgotPasswordVerifyView.as_view(), name="forgot-verify"),
    path('password/reset/', views.ResetPasswordView.as_view(), name='reset-password'),
    path('recommend/', views.RecommendationView.as_view(), name='recommendations'),
    path('articles/popular/', views.PopularAuthorsView.as_view(), name='popular-authors'),
    path('<int:id>/follow/', views.AuthorFollowView.as_view(), name='author_follow'),
    path('followers/', views.FollowersListView.as_view(), name='following-list'),
    path('following/', views.FollowingListView.as_view(), name='following-list'),
    path('notifications/', views.UserNotificationView.as_view(), name='user-notifications'),
    path('notifications/<int:pk>/', views.UserNotificationDetailView.as_view(), name='user-notification-detail'),
]