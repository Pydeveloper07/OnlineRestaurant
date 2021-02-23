from accounts.api.serializers import UserSerializer
from fantasy_restaurant.settings import JWT_TOKEN_EXPIRATION_TIME


def jwt_response_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data,
        'expiry_time': JWT_TOKEN_EXPIRATION_TIME.total_seconds()*1000 # In milliseconds
    }
