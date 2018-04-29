import io
import random
import string

from django.contrib.auth.models import User

DEFAULT_CHAR_POOL = string.ascii_uppercase + string.digits
SYSTEM_USER = None


def generate_random_string(char_pool=DEFAULT_CHAR_POOL, length=24):
    return ''.join(random.choice(char_pool) for _ in range(length))


def convert_string_content_to_stream(string_content):
    output = io.BytesIO()
    output.write(string_content)
    output.seek(0)
    return output


def get_or_create_system_user():
    global SYSTEM_USER

    # get from cache
    if isinstance(SYSTEM_USER, User):
        return SYSTEM_USER

    # get from database or create
    try:
        system_user = User.objects.get(username=u'system_user')
    except User.DoesNotExist:
        system_user = User(username=u'system_user')
        system_user.save()

    # cache and return
    SYSTEM_USER = system_user
    return SYSTEM_USER