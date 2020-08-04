from django.contrib import messages
from django.http import *
from django.shortcuts import render

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
            messages.success(request, "Your message has been succesfully sent, Thank you")
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
