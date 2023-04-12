from django.urls import path
from . import views

urlpatterns = [
    path('video/', views.VideoList.as_view(), name='index'),
    path('video/<int:pk>/', views.VideoDetail.as_view(), name='index'),
    path('alluser/',views.AllUsers.as_view(), name='allusers'),
    path('alluser/<int:pk>/', views.AllUsersDetails.as_view(),name='allusersdetails'),
]
