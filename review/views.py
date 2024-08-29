from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Review
from .forms import ReviewForm
from django.core.exceptions import PermissionDenied
from django.contrib import messages


@login_required
def submit_review(request):
    """
    Handle the submission of a new review by an authenticated user.

    GET: Render the review submission form.
    POST: Validate and save the review, then redirect to the review list.
    """
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(
                request, 'Thank you. Your review has been submitted'
            )
            return redirect('review_list')
    else:
        form = ReviewForm()
    return render(request, 'review/submit_review.html', {'form': form})


def review_list(request):
    """
    Display a list of all reviews, ordered by creation date.

    GET: Render the list of reviews.
    """
    reviews = Review.objects.all().order_by('-created_on')
    rating_range = range(1, 6)
    return render(
        request,
        'review/review_list.html',
        {'reviews': reviews, 'rating_range': rating_range}
    )


@login_required
def edit_review(request, review_id):
    """
    Handle the editing of an existing review by its owner.

    GET: Render the review editing form if the user is the owner.
    POST: Validate and save the updated review, then redirect to the review
    list.
    """
    review = get_object_or_404(Review, id=review_id)

    if review.user != request.user:
        raise PermissionDenied

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request,
                             'Thank you. Your review has been updated')

            return redirect('review_list')
    else:
        form = ReviewForm(instance=review)

    return render(request, 'review/edit_review.html', {'form': form})


@login_required
def delete_review(request, review_id):
    """
    Handle the deletion of a review by its owner.

    GET: Render a confirmation page if the user is the owner.
    POST: Delete the review and redirect to the review list.
    """
    review = get_object_or_404(Review, id=review_id)

    if review.user != request.user:
        raise PermissionDenied

    if request.method == "POST":
        review.delete()
        messages.success(request, 'Review deleted successfully.')
        return redirect('review_list')
    else:
        return render(request, 'review/confirm_delete.html',
                      {'review': review})

