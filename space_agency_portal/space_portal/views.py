from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Mission, Astronaut, Launch, NewsArticle, SpacecraftGallery, ContactMessage
from .forms import ContactForm, LoginForm, RegisterForm
from django.contrib.auth.models import User
import json


def home(request):
    featured_missions = Mission.objects.filter(status='active')[:3]
    latest_news = NewsArticle.objects.filter(is_featured=True)[:3]
    upcoming_launches = Launch.objects.filter(status='scheduled').order_by('launch_datetime')[:3]
    total_missions = Mission.objects.count()
    active_astronauts = Astronaut.objects.filter(status='active').count()
    completed_missions = Mission.objects.filter(status='completed').count()
    is_admin = False
    if request.user.is_authenticated:
        profile = getattr(request.user, 'userprofile', None)
        is_admin = request.user.is_staff or (profile and profile.role == 'admin')
    context = {
        'featured_missions': featured_missions,
        'latest_news': latest_news,
        'upcoming_launches': upcoming_launches,
        'total_missions': total_missions,
        'active_astronauts': active_astronauts,
        'completed_missions': completed_missions,
        'is_admin': is_admin,
    }
    return render(request, 'space_portal/home.html', context)


def missions(request):
    status_filter = request.GET.get('status', '')
    type_filter = request.GET.get('type', '')
    search_query = request.GET.get('q', '')

    missions_qs = Mission.objects.all()
    if status_filter:
        missions_qs = missions_qs.filter(status=status_filter)
    if type_filter:
        missions_qs = missions_qs.filter(mission_type=type_filter)
    if search_query:
        missions_qs = missions_qs.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

    context = {
        'missions': missions_qs,
        'status_filter': status_filter,
        'type_filter': type_filter,
        'search_query': search_query,
        'status_choices': Mission.STATUS_CHOICES,
        'type_choices': Mission.MISSION_TYPE_CHOICES,
    }
    return render(request, 'space_portal/missions.html', context)


def mission_detail(request, slug):
    mission = get_object_or_404(Mission, slug=slug)
    astronauts = mission.astronauts.all()
    launches = mission.launches.all()
    context = {
        'mission': mission,
        'astronauts': astronauts,
        'launches': launches,
    }
    return render(request, 'space_portal/mission_detail.html', context)


def astronauts(request):
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('q', '')
    astronauts_qs = Astronaut.objects.all()
    if status_filter:
        astronauts_qs = astronauts_qs.filter(status=status_filter)
    if search_query:
        astronauts_qs = astronauts_qs.filter(Q(name__icontains=search_query) | Q(nationality__icontains=search_query))

    context = {
        'astronauts': astronauts_qs,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    return render(request, 'space_portal/astronauts.html', context)


def astronaut_detail(request, pk):
    astronaut = get_object_or_404(Astronaut, pk=pk)
    context = {'astronaut': astronaut}
    return render(request, 'space_portal/astronaut_detail.html', context)


def launches(request):
    upcoming = Launch.objects.filter(status='scheduled').order_by('launch_datetime')
    past = Launch.objects.filter(status='launched').order_by('-launch_datetime')[:10]
    context = {
        'upcoming_launches': upcoming,
        'past_launches': past,
    }
    return render(request, 'space_portal/launches.html', context)


def news(request):
    category_filter = request.GET.get('category', '')
    search_query = request.GET.get('q', '')
    news_qs = NewsArticle.objects.all()
    if category_filter:
        news_qs = news_qs.filter(category=category_filter)
    if search_query:
        news_qs = news_qs.filter(Q(title__icontains=search_query) | Q(summary__icontains=search_query))

    context = {
        'articles': news_qs,
        'category_filter': category_filter,
        'search_query': search_query,
        'categories': NewsArticle.CATEGORY_CHOICES,
    }
    return render(request, 'space_portal/news.html', context)


def news_detail(request, slug):
    article = get_object_or_404(NewsArticle, slug=slug)
    related = NewsArticle.objects.filter(category=article.category).exclude(pk=article.pk)[:3]
    context = {'article': article, 'related_articles': related}
    return render(request, 'space_portal/news_detail.html', context)


def gallery(request):
    spacecraft = SpacecraftGallery.objects.all()
    context = {'spacecraft': spacecraft}
    return render(request, 'space_portal/gallery.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent! We will get back to you soon.')
            return redirect('contact')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()
    return render(request, 'space_portal/contact.html', {'form': form})


def about(request):
    return render(request, 'space_portal/about.html')


@login_required
def admin_dashboard(request):
    profile = getattr(request.user, 'userprofile', None)
    if not (request.user.is_staff or (profile and profile.role == 'admin')):
        messages.error(request, 'Administrator access only.')
        return redirect('home')

    context = {
        'missions': Mission.objects.all(),
        'astronauts': Astronaut.objects.all(),
        'launches': Launch.objects.all(),
        'articles': NewsArticle.objects.all(),
        'spacecraft': SpacecraftGallery.objects.all(),
        'contacts': ContactMessage.objects.all(),
        'users': User.objects.all().select_related('userprofile'),
        'total_missions': Mission.objects.count(),
        'active_astronauts': Astronaut.objects.filter(status='active').count(),
        'completed_missions': Mission.objects.filter(status='completed').count(),
        'total_articles': NewsArticle.objects.count(),
        'total_spacecraft': SpacecraftGallery.objects.count(),
        'total_contacts': ContactMessage.objects.count(),
    }
    return render(request, 'space_portal/admin_dashboard.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to COSMOSX!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def api_mission_stats(request):
    data = {
        'total': Mission.objects.count(),
        'active': Mission.objects.filter(status='active').count(),
        'completed': Mission.objects.filter(status='completed').count(),
        'planned': Mission.objects.filter(status='planned').count(),
    }
    return JsonResponse(data)
