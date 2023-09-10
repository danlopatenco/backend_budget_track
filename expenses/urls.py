from django.urls import path
from .views import CategoryAPIView, SubCategoryAPIView, ExpenseAPIView

urlpatterns = [
    path('categories/', CategoryAPIView.as_view(), name='categories'),
    path('categories/<int:pk>/', CategoryAPIView.as_view(), name='categories'),
    path('subcategory/<int:category_id>/', SubCategoryAPIView.as_view(), name='subcategory'),
    path('subcategory/<int:category_id>/<int:subcategory_id>/', SubCategoryAPIView.as_view(), name='subcategory-post'),

    path('add_expense/', ExpenseAPIView.as_view(), name='add_expense')
]
