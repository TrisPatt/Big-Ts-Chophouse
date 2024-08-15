from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import CombinedUserProfileForm
from django.contrib.auth.models import User
from django.contrib import messages

# Update profile information
def profile_update(request):
    # Get or create a user profile for the logged-in user
    user = request.user
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    # If form data is submitted, process the form
    if request.method == 'POST':
        form = CombinedUserProfileForm(request.POST, user=user, profile=profile)
        if form.is_valid():
            form.save()
            # Redirect to a success page 
            return redirect ('profile_confirmed')
    else:
        # If the request is GET, render the form with existing profile data
        form = CombinedUserProfileForm(user=user, profile=profile)
    
    return render (request, 'user_profile/profile_update.html', {'form': form})

# Confirm updates
def profile_update_confirmation(request):
    return render(request, 'user_profile/profile_confirmation.html')

# Delete user account
@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect('home')  
    return render(request, 'user_profile/delete_account.html')