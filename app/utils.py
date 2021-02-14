import random
import string
from app.constants import STORAGE_BUCKET


def random_id(length):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def generate_name(file_name):
    file_name_list = file_name.split('.')

    new_file_name = ""

    for word in file_name_list[:len(file_name_list)-1]:
        new_file_name += word

    new_file_name += '-' + random_id(8) + '.' + file_name_list[len(file_name_list) - 1]
    return new_file_name


def get_gsc_uri(file_name):
    return "gs://" + STORAGE_BUCKET + "/" + file_name


