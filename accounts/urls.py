from django.urls import path
from .views import UserView, AuthView

urlpatterns = [
    path('user-list', UserView.as_view({'get': 'get_user_list'})),
    path('auth/register', AuthView.as_view({'post': 'register'})),
    path('auth/login', AuthView.as_view({'post': 'login'})),
]
