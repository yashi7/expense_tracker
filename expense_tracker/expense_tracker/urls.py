from django.contrib import admin
from django.urls import path
from budget.views import expense_list, register, login_view, logout_view, add_expense,edit_expense,delete_expense,index  # Import your views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('expenses/', expense_list, name='expense_list'),
    path('add_expense/', add_expense, name='add_expense'),  # New expense page
    path('edit_expense/<int:expense_id>/', edit_expense, name='edit_expense'),
    path('delete_expense/<int:expense_id>/', delete_expense, name='delete_expense'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
