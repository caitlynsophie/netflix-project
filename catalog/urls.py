from django.urls import path
from . import views

urlpatterns = [
    path('', views.title_list, name='title_list'),
    path('title/<int:pk>/', views.title_detail, name='title_detail'),
    path('title/create/', views.title_create, name='title_create'),
    path('title/<int:pk>/update/', views.title_update, name='title_update'),
    path('title/<int:pk>/delete/', views.title_delete, name='title_delete'),
    path('title/<int:pk>/review/', views.review_title, name='review_title'),
    path('diary/', views.diary, name='diary'),
]