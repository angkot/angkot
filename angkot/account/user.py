from uuid import uuid4

from social_auth.models import UserSocialAuth
from social_auth.utils import setting, module_member

def get_username(user=None, user_exists=UserSocialAuth.simple_user_exists,
                 *args, **kwargs):
    if user:
        return {'username': UserSocialAuth.user_username(user)}

    prefix = setting('ACCOUNT_USERNAME_PREFIX', 'user')
    max_length = UserSocialAuth.username_max_length()
    uuid_length = setting('SOCIAL_AUTH_UUID_LENGTH', 16)

    username = None
    while username is None or user_exists(username=username):
        username = prefix + uuid4().get_hex()[:uuid_length]
        username = username[:max_length]

    return {'username': username}

