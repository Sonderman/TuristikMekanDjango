from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import *
from django.shortcuts import render
from home.forms import SignUpForm
from home.models import *


def index(request):
    setting = Setting.objects.get(pk=1)
    # category = Category.objects.all()
    context = {
        "setting": setting
    }
    return render(request, 'index.html', context)


def aboutus(request):
    setting = Setting.objects.get(pk=1)
    # category = Category.objects.all()
    context = {
        "setting": setting
    }
    return render(request, 'hakkimizda.html', context)


def references(request):
    setting = Setting.objects.get(pk=1)
    # category = Category.objects.all()
    context = {
        "setting": setting
    }
    return render(request, 'referanslar.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Mesajınız başarıyla alınmıştır, teşekkürler.")
            return HttpResponseRedirect('/contact')
    form = ContactForm()
    setting = Setting.objects.get(pk=1)
    context = {'form': form, "setting": setting}

    return render(request, 'iletisim.html', context)


def faq(request):
    fq = FAQ.objects.filter(status='True').order_by('ordernumber')
    setting = Setting.objects.get(pk=1)
    context = {'faq': fq, "setting": setting}

    return render(request, 'SSS.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Giriş Başarısız!!")
            return HttpResponseRedirect('/login')
    setting = Setting.objects.get(pk=1)
    context = {"setting": setting}
    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            user_profile = UserProfile()
            user_profile.user = user
            user_profile.phone = 0
            user_profile.image = "assets/User.jpg"
            user_profile.save()
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Hata Oldu!!<br>" + str(form.errors))
    form = SignUpForm()
    setting = Setting.objects.get(pk=1)
    context = {"setting": setting, 'form': form}
    return render(request, 'signup.html', context)
