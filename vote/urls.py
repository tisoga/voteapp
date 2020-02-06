from django.urls import path, include
from . import views
app_name = 'vote'

urlpatterns = [
    path('api/', include('vote.api.urls')),
    path('', views.ListPertanyaan, name='ListPertanyaan'),
    path('tambah_pertanyaan', views.TambahPertanyaan, name='TambahPertanyaan'),
    path('pertanyaan/<id_pertanyaan>', views.Voting, name='Voting'),
    path('pertanyaan/<id_pertanyaan>/tambah_pilihan', views.TambahPilihan, name='TambahPilihan'),
]