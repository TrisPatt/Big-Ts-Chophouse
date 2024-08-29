from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import CombinedUserProfileForm
from django.contrib.auth.models import User
from django.contrib import messages


def profile_update(request):
    """
    Handles the update of user profile information.

    Retrieves the user's profile, initializes the form with existing data,
    and saves the changes if the form is submitted and valid.

    """
    user = request.user
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = CombinedUserProfileForm(
                request.POST, user=user, profile=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_confirmed')
    else:
        form = CombinedUserProfileForm(user=user, profile=profile)

    return render(request, 'user_profile/profile_update.html', {'form': form})


def profile_update_confirmation(request):
    """
    Renders a confirmation page after successful profile update.

    """
    return render(request, 'user_profile/profile_confirmation.html')


def my_account(request):
    """
    Renders the user's account page.
    """
    return render(request, 'user_profile/account.html')


@login_required
def delete_account(request):
    """
    Handles the deletion of a user account.

    The user's account is deleted. A success message
    is shown, and the user is redirected to the home page.
    """
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect('home')
    return render(request, 'user_profile/delete_account.html')
    