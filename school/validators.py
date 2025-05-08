import re
from rest_framework.exceptions import ValidationError


class CourseLessonValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, attrs):
        value = attrs.get(self.field)

        if value is None or value == '':
            return

        if not isinstance(value, str):
            raise ValidationError({'link': ['Ссылка должна быть строкой']})

        youtube_pattern = r'^https?://(?:www\.)?(?:youtube\.com|youtu\.be)/'

        urls = re.findall(r'https?://\S+', value)
        for url in urls:
            if not re.match(youtube_pattern, url):
                raise ValidationError(
                    {'link': ['Разрешены только YouTube ссылки']}
                )
