from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Review
from .forms import ReviewForm

@login_required
def submit_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('review_list')  
    else:
        form = ReviewForm()
    return render(request, 'review/submit_review.html', {'form': form})

def review_list(request):
    reviews = Review.objects.all().order_by('-created_on')
    return render(request, 'review/review_list.html', {'reviews': reviews})