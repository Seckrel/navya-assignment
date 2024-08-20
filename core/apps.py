from django.apps import AppConfig
from django.db.models.signals import post_migrate


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self) -> None:
        post_migrate.connect(self.create_manager_group, sender=self)
        return super().ready()

    def create_manager_group(self, **kwargs):
        from django.contrib.auth.models import Group
        Group.objects.get_or_create(name='Manager')
