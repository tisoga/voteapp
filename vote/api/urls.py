from django.urls import path
from vote.api import views
from knox import views as knox_views

urlpatterns = [
    path('auth/register/', views.RegisterAPI, name='api_register'),
    path('auth/login/', views.LoginAPI, name='api_login'),
    path('auth/logout/', knox_views.LogoutView.as_view(), name='api_logout'),
    path('auth/user/', views.UserAPI, name='api_user'),
    path('data_vote/', views.ListVoteAPI, name='api_data'),
    path('data_vote/<int:id_pertanyaan>/', views.DetailVoteAPI, name='api_detail'),
    path('data_vote/<int:id_pertanyaan>/vote/', views.VotingAPI, name='api_vote')
]