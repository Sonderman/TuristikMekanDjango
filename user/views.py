from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from home.models import *
from mekan.models import *
from user.forms import UserUpdateForm, ProfileUpdateForm


def common():
    setting = Setting.objects.get(pk=1)
    # category = Category.objects.all()
    return {'setting': setting,
            # 'category': category
            }


def index(request):
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'profile': profile}
    context.update(common())
    return render(request, 'User/profile_main.html', context)


def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Hesabınız başarıyla güncellendi.")
            return redirect('/user/profile')
    else:

        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        context.update(common())
        return render(request, 'User/update_profile.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Şifreniz başarıyla değiştirildi.")
            return redirect('change_password')
        else:
            messages.warning(request, "Hata!!.<br>" + str(form.errors))
            return redirect('change_password')
    else:
        form = PasswordChangeForm(request.user)
        context = {
            'form': form,
        }
        context.update(common())
        return render(request, 'User/change_password.html', context)


@login_required(login_url='/login')
def addplaces(request):
    if request.method == 'POST':
        form = PlaceForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            data = Place()
            data.user_id = current_user.id
            data.title = form.cleaned_data['title']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.slug = form.cleaned_data['slug']
            data.detail = form.cleaned_data['detail']
            data.status = 'False'
            data.category_id = form.cleaned_data['category'].id
            data.save()
            messages.success(request, "Mekan başarıyla eklendi.")
            return HttpResponseRedirect("/user/places")
        else:
            messages.warning(request, "Error:" + str(form.errors))
            return HttpResponseRedirect("/user/addplace")
    else:
        form = PlaceForm()
        context = {
            'form': form,
        }
        context.update(common())
        return render(request, 'User/add_placePage.html', context)


@login_required(login_url='/login')
def places(request):
    # menu = Menu.objects.all()
    place = Place.objects.filter(user_id=request.user.id)
    context = {
        'places': place,
    }
    context.update(common())
    return render(request, 'User/placesPage.html', context)


@login_required(login_url='/login')
def placeedit(request, id):
    place = Place.objects.get(id=id)
    if request.method == 'POST':
        form = PlaceForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            place = form.save(commit=False)
            place.status = 'False'
            place.save()
            messages.success(request, "Mekan başarıyla değiştirildi.")
            return HttpResponseRedirect("/user/places")
        else:
            messages.warning(request, "Error:" + str(form.errors))
            return HttpResponseRedirect("/user/placeedit/" + str(id))
    else:
        form = PlaceForm(instance=place)
        context = {
            'form': form,
        }
        context.update(common())
        return render(request, 'User/add_placePage.html', context)


@login_required(login_url='/login')
def placedelete(request, id):
    Place.objects.filter(id=id, user_id=request.user.id).delete()
    messages.success(request, "Mekan silindi.")
    return HttpResponseRedirect('/user/places')


@login_required(login_url='/login')
def comments(request):
    current_user = request.user
    comment = Comment.objects.filter(user_id=current_user.id, status='True')
    context = {
        'comments': comment,
    }
    context.update(common())
    return render(request, 'User/commentsPage.html', context)


@login_required(login_url='/login')
def delete_comment(request, id):
    current_user = request.user
    Comment.objects.get(id=id, user_id=current_user.id).delete()
    messages.success(request, "Yorumunuz başarıyla Silindi.")
    return HttpResponseRedirect('/user/comments')
