from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


from mekan.models import *


@login_required(login_url='/login')
def addcomment(request, id):
    current_user_profil = UserProfile.objects.get(user_id=request.user.id)
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            current_user = request.user
            data = Comment()
            data.user_id = current_user.id
            data.userprofil = current_user_profil
            data.place_id = id
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            try:
                data.save()
            except:
                messages.warning(request, "Hata oldu!!")
                return HttpResponseRedirect(url)
            messages.success(request, "Değerlendirmeniz başarıyla alındı Teşekkürler.")
            return HttpResponseRedirect(url)
    messages.warning(request, "Girdileri kontrol edin!!")
    return HttpResponseRedirect(url)


