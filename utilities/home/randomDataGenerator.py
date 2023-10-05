import random
import string


def emailGenerator(y):
    email = ''.join(random.choice(string.ascii_lowercase) for x in range(y))
    return "auto_" + email + "@cwbqa.com"


def phoneGenerator():
    phone = f'{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}'
    # phone = ''.join(random.choice(string.digits) for x in range(10))
    return phone
