from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
        path('', views.Home.as_view(), name='home'),
        path('register/', views.Register.as_view(), name='register'),
        path('login/', views.Login.as_view(), name='login'),
        path('logout/', auth_views.LogoutView.as_view(), name='logout'),
        path('movie_list/', views.MovieView.as_view(), name='movie_list'),
        path('search/', views.Search.as_view(), name='search'),
        path('filter/', views.FilterMovie.as_view(), name='filter'),
        path('<slug:slug>/', views.MovieDetailView.as_view(), name='movie_detail'),
        path('review/<int:pk>/', views.AddReview.as_view(), name="add_review"),
]
