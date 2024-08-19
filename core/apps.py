from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self) -> None:
        self.create_manager_group()
        return super().ready()

    def create_manager_group(self):
        from django.contrib.auth.models import Group
        Group.objects.get_or_create(name='Manager')
