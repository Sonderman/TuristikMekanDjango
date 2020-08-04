from django.contrib import admin

from home.models import *


class ContactFormMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status']
    list_filter = ['status']


class FAQAdmin(admin.ModelAdmin):
    list_display = ['ordernumber', 'question', 'answer', 'status']
    list_filter = ['status']


admin.site.register(Setting)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(ContactFormMessage, ContactFormMessageAdmin)
