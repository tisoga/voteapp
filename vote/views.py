from django.shortcuts import render, get_object_or_404, redirect
from .models import PertanyaanModel, PilihanModel
# Create your views here.


def ListPertanyaan(request):
    pertanyaan = PertanyaanModel.objects.all()
    return render(request=request,
                  template_name='html/ListPertanyaan.html',
                  context={'kumpulan_pertanyaan': pertanyaan})

def Voting(request, id_pertanyaan):
    if request.method == 'POST':
        if request.POST.get('vote'):
            id = request.POST.get('vote')
            pilihan = PilihanModel.objects.get(pk=id)
            pilihan.vote += 1
            pilihan.save()
    pertanyaan = get_object_or_404(PertanyaanModel, pk=id_pertanyaan)
    pertanyaan.kumpulanpilihan = pertanyaan.pilihan.all()
    return render(request=request,
                  template_name='html/Voting.html',
                  context= {'pertanyaan': pertanyaan, 'id': id_pertanyaan})

def TambahPertanyaan(request):
    if request.method == 'POST':
        if request.POST.get('pertanyaan'):
            pertanyaan = request.POST.get('pertanyaan')
            new = PertanyaanModel.objects.create(pertanyaan = pertanyaan)
            return redirect('vote:Voting', new.id_pertanyaan)
    return render(request=request,
                  template_name='html/TambahPertanyaan.html')

def TambahPilihan(request, id_pertanyaan):
    pertanyaan = get_object_or_404(PertanyaanModel, pk = id_pertanyaan)
    if request.method == 'POST':
        if request.POST.get('pilihan'):
            pilihan = request.POST.get('pilihan')
            PilihanModel.objects.create(pilihan = pilihan, pertanyaan = pertanyaan)
            return redirect('vote:Voting', id_pertanyaan)
    return render(request=request,
                  template_name='html/TambahPilihan.html')