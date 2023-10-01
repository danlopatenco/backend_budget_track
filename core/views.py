from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import UserProfile
from .serializers import UserProfileSerializer


class UserProfileAPIView(APIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_obj = request.user
        user_profile = UserProfile.objects.get(user=user_obj)
        serializer = self.serializer_class(user_profile)
        serialized_data = serializer.data

        return Response(serialized_data)
