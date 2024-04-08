from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from myapp.views import (
    UserViewSet, LoginView, UserProfileView, EventCreateViewSet, EventsJoinedView,
    EventViewSet, UserIdView, join_event, get_participants, leave_event  # Importa la nueva vista leave_event
)
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
    path('leave-event/', leave_event, name='leave-event'),  # Agrega la URL para leave_event
    path('check-joined/', views.check_joined, name='check_joined'),
    path('cancel-event/', views.cancel_event, name='cancel_event'),


    path('event/<int:event_id>/participants', get_participants, name='get_participants'),
    path('check_email/', views.check_email, name='check_email'),

    path('reset_password/', views.reset_password, name='reset_password'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('events/user_subscribed_events/', EventViewSet.as_view({'get': 'user_subscribed_events'}), name='user-subscribed-events'),

    path('api/eventsjoined/', EventsJoinedView.as_view()),
    path('api/eventsjoined/delete/', views.delete_notification, name='delete_notification'),

    # uRL para la vista de actualización de usuario
    path('update-user/<str:username>/', views.update_user, name='update_user'),
]
