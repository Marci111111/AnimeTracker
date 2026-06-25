from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Anime, UserAnime, Genre, Studio, Review
from .forms import RegisterForm, UserAnimeForm, ReviewForm


def anime_list(request):
    query = request.GET.get('q', '')
    genre_id = request.GET.get('genre', '')
    anime_qs = Anime.objects.select_related('studio').prefetch_related('genres')
    if query:
        anime_qs = anime_qs.filter(title__icontains=query)
    if genre_id:
        anime_qs = anime_qs.filter(genres__id=genre_id)

    user_anime_ids = set()
    if request.user.is_authenticated:
        user_anime_ids = set(
            UserAnime.objects.filter(user=request.user).values_list('anime_id', flat=True)
        )

    genres = Genre.objects.all()
    selected_genre = Genre.objects.filter(pk=genre_id).first() if genre_id else None

    return render(request, 'anime/anime_list.html', {
        'anime_list': anime_qs,
        'query': query,
        'user_anime_ids': user_anime_ids,
        'genres': genres,
        'selected_genre': selected_genre,
    })


def anime_detail(request, anime_id):
    anime = get_object_or_404(Anime.objects.select_related('studio').prefetch_related('genres', 'episode_set'), pk=anime_id)
    reviews = anime.reviews.select_related('user').all()
    user_review = None
    user_entry = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
        user_entry = UserAnime.objects.filter(user=request.user, anime=anime).first()
    return render(request, 'anime/anime_detail.html', {
        'anime': anime,
        'reviews': reviews,
        'user_review': user_review,
        'user_entry': user_entry,
    })


def genre_list(request):
    genres = Genre.objects.prefetch_related('anime_set').all()
    return render(request, 'anime/genre_list.html', {'genres': genres})


def studio_list(request):
    studios = Studio.objects.prefetch_related('anime_set').all()
    return render(request, 'anime/studio_list.html', {'studios': studios})


@login_required
def my_list(request):
    status_filter = request.GET.get('status', '')
    entries = UserAnime.objects.filter(user=request.user).select_related('anime')
    if status_filter:
        entries = entries.filter(status=status_filter)
    return render(request, 'anime/my_list.html', {
        'entries': entries,
        'status_filter': status_filter,
        'status_choices': UserAnime.STATUS_CHOICES,
    })


@login_required
def add_to_list(request, anime_id):
    anime = get_object_or_404(Anime, pk=anime_id)
    entry, created = UserAnime.objects.get_or_create(user=request.user, anime=anime)

    if request.method == 'POST':
        form = UserAnimeForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{anime.title}" aggiunto/aggiornato nella tua lista.')
            return redirect('my_list')
    else:
        form = UserAnimeForm(instance=entry)

    return render(request, 'anime/add_to_list.html', {
        'form': form,
        'anime': anime,
        'created': created,
    })


@login_required
def remove_from_list(request, anime_id):
    entry = get_object_or_404(UserAnime, user=request.user, anime_id=anime_id)
    anime_title = entry.anime.title
    entry.delete()
    messages.success(request, f'"{anime_title}" rimosso dalla tua lista.')
    return redirect('my_list')


@login_required
def add_review(request, anime_id):
    anime = get_object_or_404(Anime, pk=anime_id)
    existing = Review.objects.filter(user=request.user, anime=anime).first()
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=existing)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.anime = anime
            review.save()
            messages.success(request, 'Recensione salvata.')
            return redirect('anime_detail', anime_id=anime.id)
    else:
        form = ReviewForm(instance=existing)
    return render(request, 'anime/add_review.html', {
        'form': form,
        'anime': anime,
        'existing': existing,
    })


@login_required
def delete_review(request, anime_id):
    review = get_object_or_404(Review, user=request.user, anime_id=anime_id)
    review.delete()
    messages.success(request, 'Recensione eliminata.')
    return redirect('anime_detail', anime_id=anime_id)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('anime_list')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Benvenuto, {user.username}!')
            return redirect('anime_list')
    else:
        form = RegisterForm()
    return render(request, 'anime/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('anime_list')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'anime_list'))
        messages.error(request, 'Credenziali non valide.')
    return render(request, 'anime/login.html')


def logout_view(request):
    logout(request)
    return redirect('anime_list')
