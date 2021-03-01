import random
import string


def code_for_email():
    """Generating random strings"""
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    return res
