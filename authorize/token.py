import string

import random


# генерация случайных строк
def code_for_email():
    res = ''.join(random.choices(string.ascii_uppercase +string.digits, k=12))
    return res

