from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-one relationship with User
    budget_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # User's budget limit
    # Add more fields as needed
    # e.g., full_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Expense(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)  # Allow null values
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return f"{self.category} - ${self.amount}"



class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associate with User
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    period = models.CharField(max_length=50)  # e.g., monthly, yearly

    def __str__(self):
        return f"{self.user.username}'s Budget - {self.amount} ({self.period})"
