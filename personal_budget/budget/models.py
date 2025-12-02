from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator

class Category(models.Model):
    CATEGORY_TYPES = [
        ('income', 'Доход'),
        ('expense', 'Расход'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100, verbose_name='Название')
    type = models.CharField(max_length=10, choices=CATEGORY_TYPES, verbose_name='Тип')
    color = models.CharField(max_length=7, default='#007bff', verbose_name='Цвет')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        
    
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

class Operation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='operations')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='operations')
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.01)],
        verbose_name='Сумма'
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    date = models.DateTimeField(default=timezone.now, verbose_name='Дата')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.category.name}: {self.amount} руб. ({self.date.strftime('%d.%m.%Y')})"
