from django.urls import path
from . import views

urlpatterns = [

    path('login/', views.userlogin, name = "login"),

    path('logout/', views.userlogout, name = 'logout'),

    path('register/', views.registeruser, name = 'register'),

    path('account/', views.account, name = 'account'),


    path('edituser/', views.editaccount, name='edituser'),


    path('addskills/', views.createskill, name='addskills'),


    path('deleteskills/<str:pk>', views.delete_skill, name='deleteskills'),


    path('', views.profiles, name='profiles'),


    path('updateskills/<str:pk>', views.update_skill, name='updateskills'),

    path('inbox', views.inbox, name='inbox'),

    path('message/<str:pk>', views.mes, name='mess'),

    path('sendmessage/<str:pk>/', views.send_message, name='sendmessage'),


    path('userprofile/<str:pk>/', views.userProfile, name='userprofile'),
]