from django.contrib import admin
from django.urls import path, include
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('import_data_to_db/', import_data_to_db),
    path('', include('main.urls'))
]
