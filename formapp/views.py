from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from random import randint
from .models import *
from .form import *


# index
def anasayfa(request):
    context = {}

    # search butonunu yapma

    btnSearch = request.GET.get("searchbtn")

    if btnSearch:
        context["Not"] = Not.objects.filter(title__icontains=btnSearch)
    else:
        context["Not"] = Not.objects.all()

    return render(request, "index.html", context)


def notEkle(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        image = request.FILES.get("image")

        if title and content and image:
            # veritabanına kaydet
            Not.objects.create(
                # forgnkeyi bağlamak gerek
                author=request.user,
                title=title,
                content=content,
                image=image,
            )

            return redirect("/")
        else:
            return redirect("ekle")

    else:
        return redirect("/")


# notDetay
def notDetail(request, formid):
    context = {}

    form = Not.objects.filter(id=formid).first()

    if form is None:
        return redirect("hata")
    else:
        context["form"] = form

    return render(request, "notDetail.html", context)


# hata
def hata(request):
    return render(request, "404.html")


# delete
def delete(request, formid):
    form = Not.objects.filter(id=formid).first()

    if form:
        if request.user == form.author:
            form.author = request.user
            form.delete()
    else:
        return redirect("hata")

    return redirect("/")


# update
def update(request, formid):
    context = {}

    upd = Not.objects.filter(id=formid).first()

    if upd is None and request.user:
        return redirect("hata")

    if request.method == "POST":
        form = updateForm(request.POST, request.FILES, instance=upd)

        if form.is_valid():
            form.save(commit=False)
            form.author = request.user
            form.save()
            print("Form Başarıyla Güncellendi")
            return redirect("/")
        else:
            print("Formda Hata Oluştu")
            return redirect("hata")

    else:
        context["form"] = updateForm(instance=upd)
        context["upd"] = upd
        return render(request, "update.html", context)


# login control
names = []


def handleLogin(username):
    username = username + str(randint(10, 200))
    names.append(username)

    if names.__len__() < 5:
        return handleLogin(username)

    else:
        return names


# register
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if username and email and password and password2:
            # kullanıcı adı kayıtlı mı ?
            islogin = User.objects.filter(username=username).first()

            if islogin:
                # functionu çağır
                names = handleLogin(username)
                mesaj = "Seçtiğiniz Kullanıcı Adı Mevcut: Öneriler: {isimler}".format(
                    isimler=names
                )
                messages.error(request, mesaj)
                return redirect("register")

            # for names i for döngüsüne alarak alt alta yazdırmak mümkün

            if password != password2:
                messages.warning(request, "Şifreler aynı olmalıdır")
                return redirect("register")

            User.objects.create_user(username=username, email=email, password=password)

            return redirect("giris")

        else:
            messages.warning(request, "Başarısız! Bilgileri Eksiksiz Doldurun")
            return redirect("register")

    return render(request, "register.html")


# login
def giris(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                # user banlıysa
                is_banned = Banlama.objects.filter(banlanan=request).first()
                if is_banned:
                    return redirect("hata")
                login(request, user)
                
                return redirect("/")

            else:
                return redirect("giris")

        else:
            messages.warning(request, "Kullanıcı Adı veya Şifre Hatalı")
            return redirect("giris")

    return render(request, "login.html")


# logout
def exit(request):
    logout(request)
    return redirect("/")


# profilPage


def profile(request, userid):
    context = {}
    user = User.objects.filter(id=userid).first()
    form = UserForm(request.POST, instance=user)

    if form.is_valid():
        form.save(commit=False)
        form.author = request.user
        form.save()
        return redirect("profil", userid)

    if user is None:
        return redirect("hata")

    if request.user != user:
        return redirect("hata")

    if request.method == "POST":
        mail = request.POST.get("mail")
        oldpassword = request.POST.get("oldpassword")
        newpassword = request.POST.get("newpassword")
        newpassword2 = request.POST.get("newpassword2")

        if mail:
            user.email = mail
            user.save()
        if oldpassword and newpassword and newpassword2:
            passpordCorrect = user.check_password(oldpassword)
            # checj_password eski şifreyi kontrol eden functiondur
            # eger eski şifre varsa aşama ikiye git
            if passpordCorrect:
                if newpassword == newpassword2:
                    user.set_password(newpassword)

                    user.save()
                    # şifre değişti girişe yönlendir
                    return redirect("giris")
                else:
                    messages.warning(request, "Şifreler Uyuşmuyor")
                    return redirect("profil", userid)

            else:
                messages.warning(request, "İlgili Kontroller sağlanamadi")
                return redirect("profil", userid)

        else:
            return redirect("profil", userid)

    else:
        context["user"] = user
        context["banneduser"] = BanUser()
        context["form"] = UserForm(instance=user)
        return render(request, "profil.html", context)


# profileindex


def profile_index(request, userid):
    context = {}
    user = User.objects.filter(id=userid).first()

    if request.method == "POST":
        banneduser = BanUser(request.POST)

        if banneduser.is_valid():
            banneduser = banneduser.save(commit=False)
            banneduser.yetkili = request.user
            banneduser.banlanan = user
            banneduser.save()
            return redirect("profil")
        else:
            return redirect("/")

    else:
        context["user"] = user
        return redirect("profil")

    # formlarım


def myForms(request):
    context = {}
    myform = Not.objects.filter(author__id=request.user.id)

    if myform is None:
        return redirect("hata")
    else:
        context["myform"] = myform

    return render(request, "myforms.html", context)


# exit
