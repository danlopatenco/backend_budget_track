
from django.db.models import Q


from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Category, Subcategory
from .serializers import CategorySerializer, SubCategorySerializer


class CategoryAPIView(APIView):
    """
    API endpoint for viewing and managing categories.
    """

    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):

        """
        Retrieve a single category or list all categories.
        """
        if pk is not None:
            # Retrieve a single category by its ID.
            category = Category.objects.get(pk=pk)
            serializer = self.serializer_class(category)
            return Response(serializer.data)
        else:
            # List all categories.
            user_obj = request.user
            categories = Category.objects.filter(Q(user_id__isnull=True) | Q(user_id=user_obj))
            serializer = self.serializer_class(categories, many=True)
            return Response(serializer.data)

    def post(self, request):
        """
        Create a new category.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Update an existing category.
        """
        category = Category.objects.get(pk=pk)
        serializer = self.serializer_class(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete an existing category.
        """
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubCategoryAPIView(APIView):
    """
    API endpoint for viewing and managing subcategories.
    """

    serializer_class = SubCategorySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, category_id=None, *args, **kwargs):
        if category_id is None:
            return Response('Must contain id', status=status.HTTP_400_BAD_REQUEST)
        try:
            category = Category.objects.get(pk=category_id)
            subcategories = Subcategory.objects.filter(category_id=category)
            serializer = self.serializer_class(subcategories, many=True)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response('Category not found', status=status.HTTP_404_NOT_FOUND)

    def put(self, request, category_id=None, subcategory_id=None, *args, **kwargs):

        if category_id is None or subcategory_id is None:
            return Response('Must contain both category_id and subcategory_id', status=status.HTTP_400_BAD_REQUEST)

        try:

            # category = Category.objects.get(pk=category_id)
            # subcategory = Subcategory.objects.get(pk=subcategory_id, category_id=category)

            return Response('POST request successful')
        except Category.DoesNotExist:
            return Response('Category not found', status=status.HTTP_404_NOT_FOUND)

        except Subcategory.DoesNotExist:
            return Response('Subcategory not found', status=status.HTTP_404_NOT_FOUND)
