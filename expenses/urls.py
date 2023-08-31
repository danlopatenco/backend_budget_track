from django.urls import path
from .views import CategoryAPIView, SubCategoryAPIView

urlpatterns = [
    path('categories', CategoryAPIView.as_view(), name='categories'),
    path('subcategory/<int:category_id>/', SubCategoryAPIView.as_view(), name='subcategory'),
    path('subcategory/<int:category_id>/<int:subcategory_id>/', SubCategoryAPIView.as_view(), name='subcategory-post')
]
