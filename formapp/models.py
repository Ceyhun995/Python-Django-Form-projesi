from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Not(models.Model):
    author = models.ForeignKey(User, verbose_name=("yazar"), on_delete=models.CASCADE)
    title = models.CharField(("Başlık"), unique=True, max_length=50)
    content = models.TextField(("İçerik"), max_length=250)
    image = models.FileField(upload_to='upload', max_length=100,blank=True)
    date = models.DateField(("Zaman"), auto_now=True)

    def __str__(self):
        return self.title
    
class Blok(models.Model):
    nedenler =models.CharField(("neden"), max_length=50)

    def __str__(self):
        return self.nedenler
    
class Banlama(models.Model):
    yetkili = models.ForeignKey(User, verbose_name=("yetkili"), on_delete=models.CASCADE)
    banlanan = models.ForeignKey(User, verbose_name=("banlanan"),blank=True,null=True,related_name="ban_user", on_delete=models.CASCADE)
    neden =models.CharField(("Neden"), blank=True, max_length=50)
    hazir_neden =models.ForeignKey(Blok, verbose_name=("blok"), on_delete=models.CASCADE)
    tarih =models.DateField(("tarih"), auto_now=True)

