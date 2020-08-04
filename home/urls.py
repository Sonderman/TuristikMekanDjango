from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('references', views.references, name='references'),
    path('contact', views.contact, name='contact'),
    path('faq/', views.faq, name='faq')
]
