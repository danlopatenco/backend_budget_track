from django.contrib import admin
from expenses.models import Category, Subcategory


@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("pk", 'name',)


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("pk", 'name', 'category_id',)
