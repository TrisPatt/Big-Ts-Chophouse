from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Review
from .forms import ReviewForm
from django.core.exceptions import PermissionDenied
from django.contrib import messages

@login_required
def submit_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, 'Thank you. Your review has been submitted')
            return redirect('review_list')  
    else:
        form = ReviewForm()
    return render(request, 'review/submit_review.html', {'form': form})

def review_list(request):
    reviews = Review.objects.all().order_by('-created_on')
    rating_range = range(1, 6)  
    return render(request, 'review/review_list.html', {'reviews': reviews, 'rating_range': rating_range})

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    # Check if the user is the owner of the review
    if review.user != request.user:
        raise PermissionDenied

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you. Your review has been updated') # Display confirmation message
            return redirect('review_list')  # Redirect to the review list after editing
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'review/edit_review.html', {'form': form})