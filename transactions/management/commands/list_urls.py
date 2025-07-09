from django.core.management.base import BaseCommand
from django.urls import get_resolver, URLPattern, URLResolver

class Command(BaseCommand):
    help = 'List all registered URLs in the project.'

    def handle(self, *args, **kwargs):
        def list_urls(urlpatterns, prefix=''):
            for pattern in urlpatterns:
                if isinstance(pattern, URLPattern):
                    self.stdout.write(prefix + str(pattern.pattern))
                elif isinstance(pattern, URLResolver):
                    list_urls(pattern.url_patterns, prefix + str(pattern.pattern))
        resolver = get_resolver()
        list_urls(resolver.url_patterns) 