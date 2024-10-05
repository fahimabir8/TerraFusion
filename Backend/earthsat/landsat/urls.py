# from django.urls import path
# from .views import get_path_row

# urlpatterns = [
#     path('get-path-row/', get_path_row, name='get_path_row'),
# ]

from django.urls import path
from .views import get_data,home

urlpatterns = [
    path('get-data/', get_data, name='get_data'),
    path('', home, name='home'),

]
