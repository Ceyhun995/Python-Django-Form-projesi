from django import forms
from .models import *
from django.contrib.auth.models import User


class updateForm(forms.ModelForm):

    class Meta:
        model = Not
        fields =["title","content","image","image"]


class UserForm(forms.ModelForm):

    class Meta:
        model =User
        fields =["username","first_name","last_name"]


class BanUser(forms.ModelForm):

    class Meta:
        model =Banlama
        fields = ["hazir_neden","neden",]