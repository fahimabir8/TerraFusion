from django.urls import path
from .views import get_path_row

urlpatterns = [
    path('get-path-row/', get_path_row, name='get_path_row'),
]