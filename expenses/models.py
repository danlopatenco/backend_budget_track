from django.db import models
from core.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=255)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users', null=True)
    emoji_text = models.CharField(max_length=255, null=True, blank=True)
    web_img = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories')
    emoji_text = models.CharField(max_length=255, null=True, blank=True)
    web_img = models.CharField(max_length=255, null=True, blank=True)


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)

    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.description} - {self.amount} - {self.category}"
