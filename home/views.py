from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import *
from django.shortcuts import render
from home.forms import SignUpForm, SearchForm
from home.models import *
from mekan.models import *
import json


def common():
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    return {'setting': setting,
            'category': category
            }


def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    sliderdata = Place.objects.filter(status='True').order_by('?')[:5]
    places = Place.objects.filter(status='True')[:20]
    context = {
        'sliderdata': sliderdata,
        "setting": setting,
        'category': category,
        'places': places,
    }
    return render(request, 'index.html', context)


def aboutus(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {
        "setting": setting, 'category': category
    }
    return render(request, 'hakkimizda.html', context)


def references(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {
        "setting": setting, 'category': category
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
            data.status = "New"
            data.save()
            messages.success(request, "Mesajınız başarıyla alınmıştır, teşekkürler.")
            return HttpResponseRedirect('/contact')
    form = ContactForm()
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'form': form, "setting": setting, 'category': category}

    return render(request, 'iletisim.html', context)


def faq(request):
    fq = FAQ.objects.filter(status='True').order_by('ordernumber')
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'faq': fq, "setting": setting, 'category': category}

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


def place_detail(request, id, slug):
    place = Place.objects.get(pk=id, status='True')
    profil = UserProfile.objects.get(user_id=place.user_id)
    recentP = Place.objects.filter(status='True').order_by('-id')[:5]
    recentCom = Comment.objects.filter(status='True').order_by('-id')[:5]
    images = Images.objects.filter(place_id=id)
    comments = Comment.objects.filter(place_id=id, status='True')
    context = {'place': place,
               'imgofplace': images,
               'comments': comments,
               'recentP': recentP,
               'recentCom': recentCom,
               'profil': profil}
    context.update(common())
    return render(request, 'placeDetail.html', context)


def category_view(request, id, slug):
    places = Place.objects.filter(category_id=id, status='True')
    context = {'places': places, 'page': 'category_view'}
    context.update(common())
    return render(request, 'categoryGallery.html', context)


def place_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']
            if catid == 0:
                places = Place.objects.filter(title__icontains=query, status='True')
            else:
                places = Place.objects.filter(title__icontains=query, category_id=catid, status='True')
            context = {'places': places}
            context.update(common())
            return render(request, 'place_search.html', context)
    return HttpResponseRedirect('/')


def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        place = Place.objects.filter(title__icontains=q, status='True')
        results = []
        for ph in place:
            photo_json = {}
            photo_json = ph.title
            results.append(photo_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def randplace(request):
    randplaceid = Place.objects.filter(status='True').order_by('?')[0]
    return HttpResponseRedirect('/place/' + str(randplaceid.id) + '/' + str(randplaceid.slug))
