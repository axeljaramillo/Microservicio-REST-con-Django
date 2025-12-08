from django.core.management.base import BaseCommand
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Create Site and Google SocialApp from env vars: GOOGLE_CLIENT_ID, GOOGLE_SECRET. Optionally DOMAIN and NAME.'

    def handle(self, *args, **options):
        from django.contrib.sites.models import Site
        try:
            from allauth.socialaccount.models import SocialApp
        except Exception as e:
            self.stderr.write('django-allauth is not installed or cannot be imported: %s' % e)
            return

        domain = os.environ.get('DOMAIN', 'localhost:8500')
        name = os.environ.get('SITE_NAME', 'Local')
        client_id = os.environ.get('GOOGLE_CLIENT_ID', '')
        secret = os.environ.get('GOOGLE_SECRET', '')

        if not client_id or not secret:
            self.stderr.write(self.style.ERROR('Environment variables GOOGLE_CLIENT_ID and GOOGLE_SECRET are required'))
            return

        site, created = Site.objects.get_or_create(id=getattr(settings, 'SITE_ID', 1), defaults={'domain': domain, 'name': name})
        if not created:
            site.domain = domain
            site.name = name
            site.save()

        app, created = SocialApp.objects.get_or_create(provider='google', name='Google - %s' % name,
                                                       defaults={'client_id': client_id, 'secret': secret})
        if not created:
            app.client_id = client_id
            app.secret = secret
            app.save()

        # Link app to site
        app.sites.add(site)

        self.stdout.write(self.style.SUCCESS('SocialApp for google configured and attached to site %s (%s)' % (site.name, site.domain)))
