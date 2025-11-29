from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import NetflixTitle
from .forms import NetflixTitleForm

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

def title_detail(request, pk):
    title = get_object_or_404(NetflixTitle, pk=pk)
    return render(request, 'catalog/title_detail.html', {'title': title})

def title_create(request):
    if request.method == 'POST':
        form = NetflixTitleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('title_list')
    else:
        form = NetflixTitleForm()
    return render(request, 'catalog/title_form.html', {'form': form, 'action': 'Create'})

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

def title_delete(request, pk):
    title = get_object_or_404(NetflixTitle, pk=pk)
    if request.method == 'POST':
        title.delete()
        return redirect('title_list')
    return render(request, 'catalog/title_confirm_delete.html', {'title': title})