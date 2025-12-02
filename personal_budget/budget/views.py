from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Category, Operation
from .forms import CategoryForm, OperationForm, RegistrationForm
from django.contrib.auth.models import User
from budget.models import Category
from django.contrib.auth import login as auth_login


@login_required
def dashboard(request):
    
    today = timezone.now()
    first_day = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    
    operations = Operation.objects.filter(
        user=request.user,
        date__range=[first_day, last_day]
    ).order_by('-date')
    

    incomes = operations.filter(category__type='income')
    expenses = operations.filter(category__type='expense')
    
    total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense
    
    
    expense_stats = expenses.values('category__name', 'category__color').annotate(
        total=Sum('amount')
    ).order_by('-total')
    
    context = {
        'operations': operations[:10],  
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'expense_stats': expense_stats,
        'current_month': today.strftime('%B %Y'),
    }
    return render(request, 'budget/dashboard.html', context)

@login_required
def categories(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'Категория добавлена!')
            return redirect('categories')
    else:
        form = CategoryForm()
    
    income_categories = Category.objects.filter(user=request.user, type='income')
    expense_categories = Category.objects.filter(user=request.user, type='expense')
    
    context = {
        'income_categories': income_categories,
        'expense_categories': expense_categories,
        'form': form,
    }
    return render(request, 'budget/categories.html', context)

@login_required
def add_operation(request):
    if request.method == 'POST':
        form = OperationForm(request.user, request.POST)
        if form.is_valid():
            operation = form.save(commit=False)
            operation.user = request.user
            operation.save()
            messages.success(request, 'Операция добавлена!')
            return redirect('dashboard')
    else:
        form = OperationForm(user=request.user)
    
    context = {
        'form': form,
        'categories': Category.objects.filter(user=request.user),
    }
    return render(request, 'budget/add_operation.html', context)

@login_required
def delete_operation(request, pk):
    operation = get_object_or_404(Operation, pk=pk, user=request.user)
    if request.method == 'POST':
        operation.delete()
        messages.success(request, 'Операция удалена!')
        return redirect('dashboard')
    return redirect('dashboard')

@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Категория удалена!')
        return redirect('categories')
    return redirect('categories')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            auth_login(request, user)
            
            
            default_categories = [
                
                {'name': 'Зарплата', 'type': 'income', 'color': '#28a745'},
                {'name': 'Фриланс', 'type': 'income', 'color': '#20c997'},
                {'name': 'Инвестиции', 'type': 'income', 'color': '#17a2b8'},
                
                
                {'name': 'Еда', 'type': 'expense', 'color': '#dc3545'},
                {'name': 'Транспорт', 'type': 'expense', 'color': '#fd7e14'},
                {'name': 'Развлечения', 'type': 'expense', 'color': '#6f42c1'},
                {'name': 'Жилье', 'type': 'expense', 'color': '#007bff'},
                {'name': 'Здоровье', 'type': 'expense', 'color': '#e83e8c'},
            ]
            
            for cat_data in default_categories:
                Category.objects.create(
                    user=user,
                    name=cat_data['name'],
                    type=cat_data['type'],
                    color=cat_data['color']
                )
            
            messages.success(request, 'Регистрация успешна! Для вас созданы начальные категории.')
            return redirect('dashboard')
    else:
        form = RegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})
