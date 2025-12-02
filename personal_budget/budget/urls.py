from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('categories/', views.categories, name='categories'),
    path('add/', views.add_operation, name='add_operation'),
    path('delete-operation/<int:pk>/', views.delete_operation, name='delete_operation'),
    path('delete-category/<int:pk>/', views.delete_category, name='delete_category'),
]