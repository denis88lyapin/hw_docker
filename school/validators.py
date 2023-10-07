import re

from rest_framework.serializers import ValidationError
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings

class URL_Validator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        url = value.get(self.field)
        youtube_pattern = r'^(https?://(?:www\.)?youtube\.com/)'
        if url:
            app_domains = getattr(settings, 'ALLOWED_HOSTS', None)
            if app_domains:
                for domain in app_domains:
                    app_pattern = rf'^(https?://(?:www\.)?{re.escape(domain)})'
                    if re.match(app_pattern, url) or re.match(youtube_pattern, url):
                        break
                else:
                    raise ValidationError(
                        'Недопустимый URL. Поддерживаются только ссылки на ваш сервис или YouTube.'
                    )
            else:
                if not re.match(youtube_pattern, url):
                    raise ValidationError(
                        'Недопустимый URL. Поддерживаются только ссылки на ваш сервис или YouTube.'
                    )
