from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Expense  # Make sure you import the Expense model
from .models import UserProfile
from django.db.models import Sum
from datetime import date
from django.db import models
from .forms import ExpenseForm 
from django.utils import timezone  # Add this line


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a UserProfile instance
            UserProfile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('expense_list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('expense_list')
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

@login_required
def expense_list(request):
    # Get the logged-in user's expenses
    expenses = Expense.objects.filter(user=request.user)
    
    total_expenses = sum(expense.amount for expense in expenses)
    monthly_expenses = sum(expense.amount for expense in expenses if expense.date.month == timezone.now().month)
    
    # Group expenses by category
    expenses_by_category = (
        expenses.values('category')
        .annotate(total=Sum('amount'))
    )

    context = {
        'expenses': expenses,
        'total_expenses': total_expenses,
        'monthly_expenses': monthly_expenses,
        'expenses_by_category': expenses_by_category,
    }
    
    return render(request, 'expense_list.html', context)
@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user  # Assuming you have a user field in your Expense model
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'add_expense.html', {'form': form})

@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    if request.method == 'POST':
        expense.amount = request.POST['amount']
        expense.category = request.POST['category']
        expense.date = request.POST['date']
        expense.description = request.POST['description']
        expense.save()
        return redirect('expense_list')
    return render(request, 'expense_form.html', {'expense': expense})

@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')
    return render(request, 'expense_confirm_delete.html', {'expense': expense})

def index(request):
    return render(request, 'index.html')