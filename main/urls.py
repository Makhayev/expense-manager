from django.urls import path
from . import views

urlpatterns = [
    path('', views.index.as_view(), name='home'),
    path('data', views.data.as_view(), name='data'),
    path('delete/<int:pk>', views.delete, name='delete'),
    path('graf', views.graf.as_view(), name='graf'),
    path('login', views.auth.as_view(), name='auth'),
    path('register', views.reg.as_view(), name='register'),
    path('logout', views.logOut.as_view(), name='logout'),
    path('export-to-csv', views.export_to_csv, name='export-to-csv'),
]