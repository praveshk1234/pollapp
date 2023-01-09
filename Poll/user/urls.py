from django.urls import path,include
from . import views

urlpatterns=[
    path('',views.index,name="index"),
    path('register/',views.registerUser,name="register"),
    path('login/',views.loginUser,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('create/',views.poll_create,name="poll-create"),
    path('detail/<str:pk>/',views.polldetail,name="poll-detail"),
    path('result/<str:pk>/',views.pollresult,name="poll-result"),
]