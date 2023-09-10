from rest_framework import serializers

from .models import Category, Subcategory, Expense


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the `Category` model.
    """
    user_id = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        fields = ('id', 'name', 'user_id', 'emoji_text', 'web_img')


class SubCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the `SubCategory` model.
    """

    class Meta:
        model = Subcategory
        fields = ('id', 'name', 'emoji_text', 'web_img')


class ExpenseSerializer(serializers.ModelSerializer):
    """
    Serializer for `Expense` model.
    """

    class Meta:
        model = Expense
        fields = ("id", "user", "category", "subcategory",
                  "amount", "description", "date")
