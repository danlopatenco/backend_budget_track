import redis
from rest_framework_simplejwt.authentication import JWTAuthentication, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken

from app.settings import REDIS_HOST, REDIS_PORT
from core.models import UserProfile

import json


class TelegramAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    def redis_save_user_data(self, email, token_data):
        # Use the HSET command to store data in the Redis hash
        self.redis_client.set(str(email), json.dumps(token_data))
        return True

    def redis_get_user_data(self, email):
        # Use the HGET command to retrieve data from the Redis hash
        user_data = self.redis_client.get(email)
        return json.loads(user_data) if user_data else None

    def get_user_profile(self, telegram_id):
        user_profile = None
        try:
            return UserProfile.objects.get(telegram_user_id=telegram_id).user
        except UserProfile.DoesNotExist:
            return user_profile

    def is_token_valid(self, request):

        jwt_authenticator = JWTAuthentication()

        try:
            return jwt_authenticator.authenticate(request)
        except InvalidToken:
            return False

    def create_token(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token),
        }

    def __call__(self, request):
        # Check if the specific header exists in the request
        if 'X-TELEGRAM-ID' in request.headers:
            # Do something with the header, if needed
            telegram_id = int(request.headers.get('X-TELEGRAM-ID'))

            user_profile = self.get_user_profile(telegram_id)

            if user_profile:
                data = self.redis_get_user_data(user_profile.email)

                token = data.get('token')
                if token:
                    request.META['HTTP_AUTHORIZATION'] = f'Bearer {token}'

                is_valid = self.is_token_valid(request)

                if not is_valid:
                    token_data = self.create_token(user_profile)
                    self.redis_save_user_data(user_profile.email, token_data)
                    request.META['HTTP_AUTHORIZATION'] = f'Bearer {token_data["access_token"]}'

        response = self.get_response(request)

        return response
