from django.shortcuts import render, redirect
from .forms import UserReg, ProfileImage, UserUpd
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = UserReg(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account {username}  was created successfully, enter username and password for login ')
            return redirect('user')
    else:
        form = UserReg()
    form = UserReg()
    return render(request, 'users/register.html', {'form': form, 'title': 'Register User'})


@login_required()
def profile(request):
    if request.method == 'POST':
        img_profile = ProfileImage(request.POST, request.FILES, instance=request.user.profile)
        upddate_user = UserUpd(request.POST, instance=request.user)
        if upddate_user.is_valid() and img_profile.is_valid():
            upddate_user.save()
            img_profile.save()
            messages.success(request, f'Changes saved successfully')
            return redirect('profile')
    else:
        img_profile = ProfileImage(instance=request.user.profile)
        upddate_user = UserUpd(instance=request.user)
    data = {
        'img_profile': img_profile,
        'update_user': upddate_user
    }
    return render(request, 'users/profile.html', data)