from django.urls import path
from . import views

urlpatterns = [
    #path('checkwrong/', views.checkwrong_view, name='checkwrong'),
    path('rank/', views.rank_view, name='rank'),
    path('wrong/', views.wrong_view, name='wrong'),
    path('submit/', views.submit_view, name='submit'),
    path('prob/', views.prob_view, name='prob'),
    path('level/', views.level_view, name='level'),
    path('chat/', views.chat_view, name='chat'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('', views.home_view, name='root'),
]
