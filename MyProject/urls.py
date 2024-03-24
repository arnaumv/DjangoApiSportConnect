"""
URL configuration for MyProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from myapp.views import UserViewSet, LoginView, UserProfileView,EventCreateViewSet, EventViewSet, UserIdView, join_event, get_participants
from myapp import views

router = DefaultRouter()
router.register(r'usuario', UserViewSet, basename='usuario')
router.register(r'event', EventCreateViewSet, basename='event')  
router.register(r'event-filter', EventViewSet, basename='event-filter') 


urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/<str:username>/', UserProfileView.as_view()),
    path('userid/<str:username>/', UserIdView.as_view(), name='user-id'),
    path('join-event/', join_event, name='join-event'),
    path('event/<int:event_id>/participants', get_participants, name='get_participants'),


    path('reset_password/', views.reset_password, name='reset_password'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),

    path('events/user_subscribed_events/', EventViewSet.as_view({'get': 'user_subscribed_events'}), name='user-subscribed-events'),

]