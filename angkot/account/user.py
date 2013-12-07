from uuid import uuid4

def get_username(strategy, details, user=None, *args, **kwargs):
    storage = strategy.storage

    if user:
        return {'username': storage.user.get_username(user)}

    prefix = strategy.setting('ACCOUNT_USERNAME_PREFIX', 'user')
    max_length = storage.user.username_max_length()
    uuid_length = strategy.setting('UUID_LENGTH', 16)

    username = None
    while username is None or storage.user.user_exists(username=username):
        username = prefix + uuid4().hex[:uuid_length]
        username = username[:max_length]

    return {'username': username}

