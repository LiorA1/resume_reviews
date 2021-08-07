from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserRegisterForm, CustomUserUpdateForm, ProfileUpdateForm

# Create your views here.

from django.conf import settings

from django.contrib.auth.decorators import login_required


def register(request):
    '''The View for register new users'''

    # print(request.method)
    # print(request.POST)

    if request.method != 'POST':
        form = CustomUserRegisterForm()

    else:
        form = CustomUserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username} Successfuly')

            return redirect(settings.LOGIN_REDIRECT_URL)

    context = {'form': form}
    return render(request, 'accounts/register.html', context=context)


@login_required
def profile(request):
    '''The View function for editing the user data and profile'''

    if request.method == 'POST':
        u_form = CustomUserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Account has been updated!')
            return redirect('accounts:profile')

    else:
        u_form = CustomUserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    if u_form.errors:
        messages.error(request, u_form.errors)
        # print("profile: u_form errors: ", u_form.errors)
    if p_form.errors:
        messages.error(request, p_form.errors)
        # print("profile: p_form errors: ", p_form.errors)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    # print("u_form :", u_form)
    # print("p_form :", p_form)

    return render(request, template_name='accounts/profile.html', context=context)
