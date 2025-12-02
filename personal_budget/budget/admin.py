from django.contrib import admin
from .models import Category, Operation

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'user', 'created_at']
    list_filter = ['type', 'user']
    search_fields = ['name']

@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ['category', 'amount', 'user', 'date']
    list_filter = ['category__type', 'user', 'date']
    search_fields = ['description', 'category__name']
    date_hierarchy = 'date'
