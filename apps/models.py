from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models import CharField, URLField, Model, EmailField


class Url(Model):
    short_name = CharField(max_length=255)
    long_name = URLField(max_length=255)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.short_name:
            self.short_name = self.get_unique_url()

        super().save(force_insert, force_update, using, update_fields)

    def __token(self):
        from string import ascii_letters, digits
        from random import choice
        return ''.join((choice(ascii_letters + digits) for i in range(7)))

    def get_unique_url(self):
        short_name = self.__token()
        while Url.objects.filter(short_name=short_name).exists():
            short_name = self.__token()
        return short_name


class User(AbstractUser):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$')
    phone = CharField(validators=[phone_regex], max_length=17, blank=True)
    email = EmailField(max_length=255, null=False, blank=False)
