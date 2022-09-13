from hashids import Hashids
from django.conf import settings

hashids = Hashids(settings.HASHIDS_SALT, min_length=10)

def h_encode(id):
    return hashids.encode(id)


def h_decode(h):
    z = hashids.decode(h)
    
    if type(h) == type(int): #For DELETE method
        return h
    
    if z:
        return z[0]


class HashIdConverter:
    regex = '[a-zA-Z0-9$|.]{10,}'

    def to_python(self, value):
        return h_decode(value)

    def to_url(self, value):
        return h_encode(value)