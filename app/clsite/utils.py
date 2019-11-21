import random
from io import BytesIO

from PIL import Image
from django.core.files import File
from django.core.files.base import ContentFile


def random_number_exponential_delay(pr=0.25, probability_of_none=0.0):
    if random.random() < probability_of_none:
        return 0

    i = 1
    while random.random() < pr:
        i += 1

    return i


def generate_image(color=(255, 0, 0)):
    # Pillow requires color to be tuple of ints
    thumb = Image.new('RGB', (200, 200), color=tuple(map(int, color)))
    thumb_io = BytesIO()
    thumb.save(thumb_io, format='JPEG')
    content = ContentFile(thumb_io.getvalue())
    return File(content.file, 'test.jpg')
