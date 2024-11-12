from . views import CSVConvertAPIView
from django.urls import path

urlpatterns = [
    path('', CSVConvertAPIView.as_view(), name='convert'),
]