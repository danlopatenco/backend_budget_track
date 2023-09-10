
from django.db.models import Q, Sum
from django.utils import timezone

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Category, Subcategory, Expense
from .serializers import CategorySerializer, SubCategorySerializer, ExpenseSerializer


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

        user_obj = request.user
        if not user_obj:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Update an existing category.
        """
        try:
            category = Category.objects.get(pk=pk)

        except Category.DoesNotExist:
            return Response('Category not found', status=status.HTTP_404_NOT_FOUND)

        if category.user_id.email != request.user.email:
            return Response("Unauthorized: You do not have the necessary permissions to modify this data.", status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(category, data=request.data, context={'request': request})
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


class ExpenseAPIView(APIView):
    """
    API endpoint for viewing and managing expenses.
    """

    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        period = request.query_params.get('period')

        start_date = self.get_period(period)
        end_date = timezone.now()

        user_id = request.user.id

        if period != 'all':
            expenses = Expense.objects.filter(date__range=(start_date, end_date), user_id=user_id)
        else:
            expenses = Expense.objects.filter(user_id=user_id).all()

        expenses_summary = expenses.values('subcategory__name').annotate(total_amount=Sum('amount'))
        total_sum = expenses_summary.aggregate(total_sum=Sum('total_amount'))['total_sum']

        if period != 'all':
            start_date_str = timezone.localtime(start_date).strftime('%Y-%m-%d')
            end_date_str = timezone.localtime(end_date).strftime('%Y-%m-%d')
        else:
            start_date_str = timezone.localtime(expenses.last().date).strftime('%Y-%m-%d')
            end_date_str = timezone.localtime(expenses.first().date).strftime('%Y-%m-%d')
        period_response = f"{start_date_str} - {end_date_str}"

        return Response({"data": expenses_summary,
                         'total_sum': total_sum,
                         "period": period_response
                         })

    def get_period(self, period):
        today = timezone.now()

        if period == 'today':
            return today.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == 'this_week':
            return today - timezone.timedelta(days=today.weekday())
        elif period == 'this_month':
            return today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        elif period == 'last_3_months':
            return today - timezone.timedelta(days=90)
        elif period == 'last_6_months':
            return today - timezone.timedelta(days=180)
        elif period == 'this_year':
            return today.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            return 'all'
