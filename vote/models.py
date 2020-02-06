from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class PertanyaanModel(models.Model):
    id_pertanyaan = models.AutoField(primary_key=True, unique=True)
    pertanyaan = models.CharField(max_length=255)
    pembuat = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.pertanyaan

    @property
    def kumpulan_pilihan(self):
        return self.pilihan.all()


class PilihanModel(models.Model):
    id_pilihan = models.AutoField(primary_key=True, unique=True)
    pertanyaan = models.ForeignKey(
        PertanyaanModel, related_name='pilihan', on_delete=models.CASCADE)
    pilihan = models.CharField(max_length=255)
    vote = models.IntegerField(default=0)

    def __str__(self):
        return self.pilihan
