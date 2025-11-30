from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import NetflixTitle, Review
from .forms import NetflixTitleForm, ReviewForm

def title_list(request):
    titles = NetflixTitle.objects.all()
    
    # Search
    search = request.GET.get('search', '')
    if search:
        titles = titles.filter(
            Q(title__icontains=search) |
            Q(cast__icontains=search) |
            Q(director__icontains=search)
        )
    
    # Filter by type
    title_type = request.GET.get('type', '')
    if title_type:
        titles = titles.filter(title_type=title_type)
    
    # Filter by genre
    genre = request.GET.get('genre', '')
    if genre:
        titles = titles.filter(genres__icontains=genre)
    
    # Sort
    sort = request.GET.get('sort', '-release_year')
    titles = titles.order_by(sort)
    
    # Get unique genres for filter dropdown
    all_genres = set()
    for title in NetflixTitle.objects.all():
        all_genres.update([g.strip() for g in title.genres.split(',')])
    
    context = {
        'titles': titles,
        'genres': sorted(all_genres),
        'search': search,
        'selected_type': title_type,
        'selected_genre': genre,
    }
    return render(request, 'catalog/title_list.html', context)

# Detail page for each title
def title_detail(request, pk):
    title = get_object_or_404(NetflixTitle, pk=pk)
    return render(request, 'catalog/title_detail.html', {'title': title})

# Add new title
def title_create(request):
    if request.method == 'POST':
        form = NetflixTitleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('title_list')
    else:
        form = NetflixTitleForm()
    return render(request, 'catalog/title_form.html', {'form': form, 'action': 'Create'})

# Submit new title
def title_update(request, pk):
    title = get_object_or_404(NetflixTitle, pk=pk)
    if request.method == 'POST':
        form = NetflixTitleForm(request.POST, instance=title)
        if form.is_valid():
            form.save()
            return redirect('title_detail', pk=pk)
    else:
        form = NetflixTitleForm(instance=title)
    return render(request, 'catalog/title_form.html', {'form': form, 'action': 'Update'})

# Delete
def title_delete(request, pk):
    title = get_object_or_404(NetflixTitle, pk=pk)
    if request.method == 'POST':
        title.delete()
        return redirect('title_list')
    return render(request, 'catalog/title_confirm_delete.html', {'title': title})

# Add review to a title
def review_title(request, pk):
    title = get_object_or_404(NetflixTitle, pk=pk)

    existing_review = Review.objects.filter(title=title).first()

    # Submit review
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.title = title
            review.save()
            return redirect('title_detail', pk=pk)  # after saving, go to details page
    else:
        # Display current review when already reviewed
        form = ReviewForm(instance=existing_review)

    return render(request, 'catalog/review_title.html', {
        'title': title,
        'form': form,
        'existing_review': existing_review,
    })

# All reviews
def diary(request):
    reviews = Review.objects.select_related('title')

    # default sort: date watched (newest first)
    sort = request.GET.get('sort', 'date')

    if sort == 'name':
        reviews = reviews.order_by('title__title')
    elif sort in ['rating', 'ranking']:
        reviews = reviews.order_by('-rating', '-date_watched', '-created_at')
    else: 
        reviews = reviews.order_by('-date_watched', '-created_at')

    context = {
        'reviews': reviews,
        'current_sort': sort,
    }
    return render(request, 'catalog/diary.html', context)
