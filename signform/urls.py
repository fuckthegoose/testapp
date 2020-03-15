from django.urls import path

from .views import LoginView, SignUpView, IndexView, LogoutView

app_name = 'signform'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('index/', IndexView.as_view(), name='index'),
    path('logout/', LogoutView.as_view(), name='logout')
]
