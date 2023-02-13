from django.core.management.base import BaseCommand
from django.utils import timezone
from smallurl.models import URL

class Command(BaseCommand):
    help = 'Deletes expired rows'
    
    def handle(self, *args, **options):
        now = timezone.now()
        URL.objects.filter(expires__lte=now).delete()