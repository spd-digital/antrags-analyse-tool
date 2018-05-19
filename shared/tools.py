# -*- coding: utf-8 -*-
"""This module provides generic tools shared across the platform."""

import io
import random
import string

from django.contrib.auth.models import User

DEFAULT_CHAR_POOL = string.ascii_uppercase + string.digits
SYSTEM_USER = None


def generate_random_string(char_pool=DEFAULT_CHAR_POOL, length=24):
    """Generates a string of variable length from a pool of characters.

    Args:
        char_pool (str): pool of characters to choose from when generating the random string
        length (int): the length of the random string

    Returns (unicode): the random string

    """
    return u''.join(random.choice(char_pool) for _ in range(length))


def convert_string_content_to_stream(string_content):
    """Returns a binary stream for a given string.

    Args:
        string_content (unicode): string content

    Returns (io.BytesIO): a binary stream

    """
    output = io.BytesIO()
    output.write(string_content)
    output.seek(0)
    return output


def get_or_create_system_user():
    """Either returns the existing system user or creates and then returns it.

    In a number of situations, processes can be triggered either by a specific user or by the system itself.
    In the latter case, the process owner should still be set. For this, we require a dedicated system user.
    This function ensures it exists and can be returned.

    Returns (User): the system user

    """
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