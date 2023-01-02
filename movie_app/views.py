import re

from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import models, decorators, authenticate, login
from django.contrib import messages
from django.views.generic import ListView, DetailView, TemplateView

from movie_site.settings import PASSWORD_PATTERN
from .forms import ReviewForm
from .logic.additional_function import *


class Home(TemplateView):
    template_name = 'movie_app/index.html'


@method_decorator(decorators.login_required, name='dispatch')
class MovieView(ListView):
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = 'movie_app/movie_list.html'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['all_genres'] = get_genres()
        context['all_years'] = get_years()
        return context


@method_decorator(decorators.login_required, name='dispatch')
class MovieDetailView(DetailView):
    model = Movie
    slug_field = 'url'
    template_name = 'movie_app/movie_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = ReviewForm()
        return context


class Register(TemplateView):
    template_name = 'movie_app/register.html'

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if re.match(PASSWORD_PATTERN, password1) is None:
            messages.error(request, '⚠️ Пароль занадто слабкий!')
            return redirect('register')

        if password1 != password2:
            messages.error(request, '⚠️ Паролі не збігаються! Спробуйте ще раз')
            return redirect('register')

        if models.User.objects.filter(username=username).exists():
            messages.error(request, '⚠️ Ім`я користувача вже існує!')
            return redirect('register')

        if models.User.objects.filter(email=email).exists():
            messages.error(request, '⚠️ Адреса електронної пошти вже існує!')
            return redirect('register')

        user = models.User.objects.create_user(username=username, email=email)
        user.set_password(password1)
        user.save()

        messages.success(request, '✅ Реєстрація успішна!')
        return redirect('login')


@method_decorator(login_forbidden, name='dispatch')
class Login(TemplateView):
    template_name = 'movie_app/login.html'

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(reverse('movie_list'))
        else:
            messages.error(request, '⚠️ Ім\'я користувача або пароль введено неправильно')
            return redirect('login')


class AddReview(View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.movie = movie
            form.name = request.user.username
            form.email = request.user.email
            form.save()
        return redirect(movie.get_absolute_url())


class Search(ListView):
    paginate_by = 6

    def get_queryset(self):
        return Movie.objects.filter(title__iregex=self.request.GET.get("search"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = f'search={self.request.GET.get("search")}&'
        return context


class FilterMovie(ListView):
    paginate_by = 8

    def get_queryset(self):
        queryset = Movie.objects.filter(draft=False)
        if 'year' in self.request.GET:
            queryset = queryset.filter(year__in=self.request.GET.getlist('year'))
        if 'genre' in self.request.GET:
            queryset = queryset.filter(genre__in=self.request.GET.getlist('genre'))
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['year'] = ''.join([f'year={x}&' for x in self.request.GET.getlist('year')])
        context['genre'] = ''.join([f'genre={x}&' for x in self.request.GET.getlist('genre')])
        context['all_years'] = get_years()
        context['all_genres'] = get_genres()
        return context
