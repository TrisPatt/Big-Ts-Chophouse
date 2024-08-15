from django.shortcuts import render, redirect
from .models import Profile
from .forms import UserProfileForm

def profile_update(request):
    # Get or create a user profile for the logged-in user
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    # If form data is submitted, process the form
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # Redirect to a success page 
            return redirect ('profile_confirmed')
    else:
        # If the request is GET, render the form with existing profile data
        form = UserProfileForm(instance=profile)
    
    return render (request, 'user_profile/profile_update.html', {'form': form})

def profile_update_confirmation(request):
    return render(request, 'user_profile/profile_confirmation.html')