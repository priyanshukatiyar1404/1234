from . views import LoginView
from django.urls import path

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    # path('signup/', SignUPview.as_view(), name='signup'),
]